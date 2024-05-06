using Emgu.CV;

namespace Pancake_Rotation_Tracker;


public class VideoFrameSplitter {
    static void ExtractImages(string PathIn, string PathOut)
    {
        int count = 0;
        VideoCapture vidcap = new VideoCapture(PathIn);
        PathOut = "./FrameExport/"+PathOut;
        Directory.CreateDirectory(PathOut);
        Console.WriteLine(vidcap);
        var img = new Mat();
        while (vidcap.Read(img))
        {
            img.Save("./"+PathOut+"/frame"+count.ToString()+".jpg");
            count++;
        }
    }
    static void Main(string[] args)
    {
        string? InputPath = null;
        string? OutputPath = null;
        //while (InputPath == null){
        //    Console.Write("Please enter videofile name: ");
        //    InputPath = Console.ReadLine();
        //}
        //while (OutputPath == null){
        //    Console.Write("Please Enter the output folder name: ");
        //    OutputPath = Console.ReadLine();
        //}
        //ExtractImages(InputPath, OutputPath);
        //Console.WriteLine("Done!");
        //Console.WriteLine("Sending Command To Rebuild Video!");
        //VideoCreator.CreateVideo(OutputPath);
        ImageProcessor ImageProcessor = new ImageProcessor();
        ImageProcessor.CheckImage("frame0.jpg","c0156",.8f);
    }
}