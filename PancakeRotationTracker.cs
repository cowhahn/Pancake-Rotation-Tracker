using System.Drawing;
using System.IO;
using Emgu.CV;

namespace Pancake_Rotation_Tracker;

public class PancakeRotationTracker{
        static void Main(string[] args){
        List<List<Point>> MarkedData = new List<List<Point>>();
        string? InputPath = null;
        while (InputPath == null){
            Console.Write("Please enter videofile name: ");
            InputPath = Console.ReadLine();
        }
        int length = VideoFrameSplitter.ExtractImages(InputPath);
        for (int i = 0; i<length; i++){
            string FrameName = "frame"+i+".jpg";
            string VideoName = InputPath;
            List<Point> SortedLoc = new List<Point>();
            List<Point> loc = ImageProcessor.CheckImage(FrameName,VideoName, .8f);
            Console.WriteLine("Processing frame: "+i);
            if (i==0) {
                SortedLoc = DataProcessor.SortPoints(loc,loc);
            }
            if (i != 0){
                SortedLoc = DataProcessor.SortPoints(MarkedData[i-1], loc);
            }
            MarkedData.Add(SortedLoc);
            Console.WriteLine(SortedLoc.Count());
        }
        Console.WriteLine("Amount of Frames: "+MarkedData.Count());
        /*foreach (List<Point> item in MarkedData){
            foreach(Point point in item){
                Console.Write(point);
            }
            Console.Write("\n");
        }*/
    }
}