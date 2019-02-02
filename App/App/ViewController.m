//
//  ViewController.m
//  CALHACKS
//
//  Created by Kevin Frans on 10/9/15.
//  Copyright © 2015 Kevin Frans. All rights reserved.
//

#import "ViewController.h"
#import <AVFoundation/AVFoundation.h>
#import <ImageIO/CGImageProperties.h>

@interface ViewController ()

@end

#define dWidth self.view.frame.size.width
#define dHeight self.view.frame.size.height

@implementation ViewController
{
    AVCaptureStillImageOutput* stillImageOutput;
    UIImageView* capturedView;
    UIButton* capture;
    UILabel* label;
    int count;
}

+ (Class)layerClass
{
    return [AVCaptureVideoPreviewLayer class];
}

- (AVCaptureDevice *)frontCamera {
    NSArray *devices = [AVCaptureDevice devicesWithMediaType:AVMediaTypeVideo];
    for (AVCaptureDevice *device in devices) {
        if ([device position] == AVCaptureDevicePositionFront) {
            return device;
        }
    }
    return nil;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    AVCaptureSession *session = [[AVCaptureSession alloc] init];
    session.sessionPreset = AVCaptureSessionPresetHigh;
    AVCaptureDevice *device = [self frontCamera];
    NSError *error = nil;
    AVCaptureDeviceInput *input = [AVCaptureDeviceInput deviceInputWithDevice:device error:&error];
    [session addInput:input];
    AVCaptureVideoPreviewLayer *newCaptureVideoPreviewLayer = [[AVCaptureVideoPreviewLayer alloc] initWithSession:session];
    newCaptureVideoPreviewLayer.videoGravity = AVLayerVideoGravityResizeAspectFill;
    newCaptureVideoPreviewLayer.frame = CGRectMake(0, 0, dWidth, dHeight);
    //    newCaptureVideoPreviewLayer.la
    [self.view.layer addSublayer:newCaptureVideoPreviewLayer];
    [session startRunning];
    
    //    capturedView = [[UIImageView alloc] initWithFrame:CGRectMake(0, 0, dWidth, dHeight)];
    //    //    capturedView.image = image;
    //    [self.view addSubview:capturedView];
    
    
    stillImageOutput = [[AVCaptureStillImageOutput alloc] init];
    NSDictionary *outputSettings = [[NSDictionary alloc] initWithObjectsAndKeys: AVVideoCodecJPEG, AVVideoCodecKey, nil];
    [stillImageOutput setOutputSettings:outputSettings];
    [session addOutput:stillImageOutput];
    
    
    [NSTimer scheduledTimerWithTimeInterval:0.1f target:self selector:@selector(tick:) userInfo:nil repeats:YES];
    
    count = 3;
    
    label = [[UILabel alloc] initWithFrame:CGRectMake(0, 500, dWidth, 100)];
    label.text = @"3";
    label.textAlignment = NSTextAlignmentCenter;
    label.font = [UIFont boldSystemFontOfSize:60];
    [self.view addSubview:label];
    
    
    
    
    // Do any additional setup after loading the view, typically from a nib.
}

-(void) tick:(NSTimer*)timer
{
    count = count - 1;
    label.text = [NSString stringWithFormat:@"%d",count];
    if(count == 0)
    {
        count = 1;
        [self capture];
    }
}


-(void) capture
{
    
    UIView* v = [[UIView alloc] initWithFrame: CGRectMake(0, 0, dWidth, dHeight)];
    [self.view addSubview: v];
    v.backgroundColor = [UIColor whiteColor];
    [UIView animateWithDuration:0.2 delay:0.0 options:
     UIViewAnimationOptionCurveEaseIn animations:^{
         v.backgroundColor = [UIColor clearColor];
     } completion:^ (BOOL completed) {
         [v removeFromSuperview];
     }];
    
    
    [[NSUserDefaults standardUserDefaults] setInteger:[[NSUserDefaults standardUserDefaults] integerForKey:@"snap"]+1 forKey:@"snap"];
    
    AVCaptureConnection *videoConnection = nil;
    for (AVCaptureConnection *connection in stillImageOutput.connections)
    {
        for (AVCaptureInputPort *port in [connection inputPorts])
        {
            if ([[port mediaType] isEqual:AVMediaTypeVideo] )
            {
                videoConnection = connection;
                break;
            }
        }
        if (videoConnection)
        {
            break;
        }
    }
    
    [stillImageOutput captureStillImageAsynchronouslyFromConnection:videoConnection completionHandler: ^(CMSampleBufferRef imageSampleBuffer, NSError *error)
     {
         CFDictionaryRef exifAttachments = CMGetAttachment( imageSampleBuffer, kCGImagePropertyExifDictionary, NULL);
         if (exifAttachments)
         {
             // Do something with the attachments.
             //             NSLog(@"attachements: %@", exifAttachments);
         } else {
             NSLog(@"no attachments");
         }
         
         NSData *imageData = [AVCaptureStillImageOutput jpegStillImageNSDataRepresentation:imageSampleBuffer];
         UIImage *image = [[UIImage alloc] initWithData:imageData];
         
         NSData *imageData2 = UIImageJPEGRepresentation(image, 0.0);
         NSString *encodedString = [imageData2 base64Encoding];
         
         NSMutableURLRequest *urlRequest = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:@"the ngrok url"]];
         
         NSString *imageData3 =[NSString stringWithFormat:@"image=%@",encodedString];
         
         //create the Method "GET" or "POST"
         [urlRequest setHTTPMethod:@"POST"];
         
         //Convert the String to Data
         NSData *data1 = [imageData3 dataUsingEncoding:NSUTF8StringEncoding];
         
         //Apply the data to the body
         [urlRequest setHTTPBody:data1];
         
         NSURLSession *session = [NSURLSession sharedSession];
         NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:urlRequest completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
             NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *)response;
             if(httpResponse.statusCode == 200)
             {
                 NSLog(@"aylmao");
             }
             else
             {
                 NSLog(@"Error");
             }
         }];
         [dataTask resume];
         
     }];
}


-(void) sendRequest:(NSURLRequest*) request
{
    NSOperationQueue *queue = [[NSOperationQueue alloc] init];
    [NSURLConnection sendAsynchronousRequest:request queue:queue completionHandler:^(NSURLResponse *response, NSData *data, NSError *error)
     {
         if (error)
         {
             NSLog(@"Error,%@", [error localizedDescription]);
         }
         else
         {
             dispatch_async(dispatch_get_main_queue(), ^{
                 //                 bg.backgroundColor = [UIColor blueColor];
                 NSLog(@"%@", [[NSString alloc] initWithData:data encoding:NSASCIIStringEncoding]);
             });
         }
     }];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
