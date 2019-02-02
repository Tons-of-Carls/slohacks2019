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

- (void)viewDidLoad {
    [super viewDidLoad];
    
    AVCaptureSession *session = [[AVCaptureSession alloc] init];
    session.sessionPreset = AVCaptureSessionPresetHigh;
    AVCaptureDevice *device = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
    NSError *error = nil;
    AVCaptureDeviceInput *input = [AVCaptureDeviceInput deviceInputWithDevice:device error:&error];
    [session addInput:input];
    AVCaptureVideoPreviewLayer *newCaptureVideoPreviewLayer = [[AVCaptureVideoPreviewLayer alloc] initWithSession:session];
    newCaptureVideoPreviewLayer.videoGravity = AVLayerVideoGravityResizeAspectFill;
    newCaptureVideoPreviewLayer.frame = CGRectMake(0, 0, dWidth, dHeight);
    [self.view.layer addSublayer:newCaptureVideoPreviewLayer];
    [session startRunning];
    
    stillImageOutput = [[AVCaptureStillImageOutput alloc] init];
    NSDictionary *outputSettings = [[NSDictionary alloc] initWithObjectsAndKeys: AVVideoCodecJPEG, AVVideoCodecKey, nil];
    [stillImageOutput setOutputSettings:outputSettings];
    [session addOutput:stillImageOutput];
    
    
    [NSTimer scheduledTimerWithTimeInterval:0.4f target:self selector:@selector(tick:) userInfo:nil repeats:YES];
    
    count = 3;
    
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
         NSURL *url = [[NSURL alloc] initWithString:@"the ngrok url"];
         
         NSMutableURLRequest *urlRequest = [[NSMutableURLRequest alloc] initWithURL:url];
         
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

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
