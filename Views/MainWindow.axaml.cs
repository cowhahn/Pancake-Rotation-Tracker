using Avalonia.Controls;
using Avalonia.Interactivity;
using System.Text;

namespace MultiobjectTemplateTracking.Views;

public partial class MainWindow : Window
{
    public static System.Drawing.Bitmap CurrentImage;
    public MainWindow()
    {
        InitializeComponent();
    }
    public double SensValue => SensitivitySelector.Value;
    public void StartClicked(object sender, RoutedEventArgs e)
    {
        AnalysisProgram.StartThreads(VideoPath.Text, TemplatePath.Text, (float)SensValue);
    }
    public void SwitchToTemplateScreen(object sender, RoutedEventArgs e)
    {
        
    }
    public async void SelectVideoFile(object sender,RoutedEventArgs e) 
    {
        var topLevel = TopLevel.GetTopLevel(this);

        var files = await topLevel.StorageProvider.OpenFilePickerAsync(new Avalonia.Platform.Storage.FilePickerOpenOptions
        {
            Title = "Open Video File",
            AllowMultiple = false
        });
        string path = files[0].Path.ToString();
        StringBuilder foo = new StringBuilder(path);
        foo.Remove(0, 8);
        path = foo.ToString();
        VideoPath.Text = path;
        //TemplateSelectScreen.IsEnabled = true;
    }
    public async void SelectTemplateFile(object sender,RoutedEventArgs e) 
    {
        var topLevel = TopLevel.GetTopLevel(this);

        var files = await topLevel.StorageProvider.OpenFilePickerAsync(new Avalonia.Platform.Storage.FilePickerOpenOptions
        {
            Title = "Open Video File",
            AllowMultiple = false
        });
        string path = files[0].Path.ToString();
        StringBuilder foo = new StringBuilder(path);
        foo.Remove(0, 8);
        path = foo.ToString();
        TemplatePath.Text = path;
    }
}