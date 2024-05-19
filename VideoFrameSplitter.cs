using Emgu.CV;
using System.Collections.Generic;

namespace MultiobjectTemplateTracking;


public class VideoFrameSplitter {
    public static int ExtractImages(string PathIn)
    {
        int count = 0;
        VideoCapture vidcap = new VideoCapture(PathIn);
        String PathOut = "./FrameExport/"+PathIn;
        Directory.CreateDirectory(PathOut);
        Console.WriteLine(vidcap);
        var img = new Mat();
        while (vidcap.Read(img))
        {
            img.Save("./"+PathOut+"/frame"+count.ToString()+".jpg");
            count++;
        }
        return count;
    }
}