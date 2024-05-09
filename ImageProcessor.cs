using System.Drawing;
using System.Runtime.CompilerServices;
using Emgu.CV;
using Emgu.CV.CvEnum;
using Emgu.CV.PpfMatch3d;
using Emgu.CV.Reg;
using Emgu.CV.Structure;

namespace Pancake_Rotation_Tracker;

public class ImageProcessor{
    static int radius = 30;
    static string TemplatePath = "./ImageTemplates/TestTemplate.png";
    static ImreadModes ImageReadType = ImreadModes.ReducedGrayscale2;
    static bool DistanceBetween(List<Point> PrevPoints, Point pos){
        foreach (Point item in PrevPoints){
            double distx = item.X-pos.X;
            double disty = item.Y-pos.Y;
            distx *= distx;
            disty *= disty;
            double dist = Math.Sqrt(distx+disty);
            if (dist<radius) return false;
        }
        return true;
    }
    public static List<Point> CheckImage(string FrameName, string VideoName, float sens){
        MCvScalar red = new MCvScalar(255,0,0);
        Mat template = CvInvoke.Imread(TemplatePath, ImageReadType);
        Mat frame = CvInvoke.Imread("./FrameExport/"+VideoName+"/"+FrameName, ImageReadType);
        List<Single> ResData = new List<Single>();
        List<Point> loc = new List<Point>();
        Mat res = new Mat();
        int h = template.Height;
        int w = template.Width;
        TemplateMatchingType[] MatchAlgorithms = [TemplateMatchingType.Ccoeff,
        TemplateMatchingType.CcoeffNormed,
        TemplateMatchingType.Sqdiff,
        TemplateMatchingType.SqdiffNormed,
        TemplateMatchingType.Ccorr,
        TemplateMatchingType.CcorrNormed];
        CvInvoke.Threshold(frame,frame,128,255,ThresholdType.Binary);
        CvInvoke.MatchTemplate(frame,template,res,MatchAlgorithms[3]);
        Single[,] PixelData = new Single[res.Height,res.Width];
        foreach (Single item in res.GetData()){
            ResData.Add(item);
        }
        int ResDataCount = ResData.Count();
        int W_0 = res.Width;
        for (int i = 0; i < ResDataCount; i++){
            if (ResData[i] <= sens){
                Point pos = new Point(i%W_0,(i/W_0)+h);
                if (DistanceBetween(loc, pos)){
                    loc.Add(pos);
                }
            }
            
        }
        return loc;
    }

}