using Emgu.CV;

namespace Pancake_Rotation_Tracker;

public class ImageProcessor{
    int beta = -50;
    float alpha = 1.2f;
    Mat template = new Mat();
    int n = 0;
    int radius = 50;

    public static void DrawRectangles(List<float> centers, Mat ImgRGB, int h, int w,int[] colors){
        foreach (var points in centers){
            //int StartPoint = ();
            //int EndPoint = ();
        
        }
    }

}