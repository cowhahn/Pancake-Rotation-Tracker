using Emgu.CV;

namespace Pancake_Rotation_Tracker;

public class VideoCreator{
    public static void CreateVideo(string VideoName){
        Mat img = new Mat();
        List<Mat> ImageList = new List<Mat>();
        var ImageReadType =  Emgu.CV.CvEnum.ImreadModes.Unchanged;
        int DefaultEncoder = VideoWriter.Fourcc('H', '2', '6', '4');
        var Files = Directory.EnumerateFiles("./"+VideoName);
        for (int i = 0; i < Files.Count(); i++)
        {
            img = CvInvoke.Imread("./"+VideoName+"/frame"+i.ToString()+".jpg", ImageReadType);
            ImageList.Add(img);
        }
        VideoWriter Writer = new VideoWriter("./MarkedVideos/"+VideoName+".mp4", DefaultEncoder, 15, img.Size, true);
        foreach (var item in ImageList){
            Writer.Write(item);
        }
        Writer.Dispose();
    }
}
