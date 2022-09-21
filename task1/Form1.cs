namespace task1;

public partial class Form1 : Form
{
    Color col;
    Bitmap img;
    Graphics g;
    Pen pen;
    bool mouseDown;
    int x, y;
    public Form1()
    {
        col = Color.Black;
        InitializeComponent();
        pen = new Pen(col, 5);
        pen.StartCap = pen.EndCap = System.Drawing.Drawing2D.LineCap.Round;
        img = new Bitmap(Width, Height);
        g = Graphics.FromImage(img);
        g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
        mouseDown = false;
    }

    private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
    {
        mouseDown = true;
        x = e.X;
        y = e.Y;
    }

    private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
    {
        mouseDown = false;
    }

    private void pictureBox1_MouseClick(object sender, MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Right)
        {
            floodFill(e.X, e.Y);
            // img.Save("image.png");
        }
    }

    private void Form1_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.KeyCode == Keys.Escape)
        {
            img = new Bitmap(Width, Height);
            g = Graphics.FromImage(img);
            pictureBox1.Image = img;
        }
    }

    private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
    {
        if (mouseDown && e.Button == MouseButtons.Left)
        {
            g.DrawLine(pen, new Point(x, y), e.Location);
            x = e.X;
            y = e.Y;
            pictureBox1.Image = img;
        }
    }

    private void floodFill(int x, int y)
    {
        Color targetColor = img.GetPixel(x, y);
        if (targetColor == col)
            return;
        Stack<Point> stack = new Stack<Point>();
        stack.Push(new Point(x, y));
        while (stack.Count > 0)
        {
            Point p = stack.Pop();
            if (img.GetPixel(p.X, p.Y) == targetColor)
            {
                img.SetPixel(p.X, p.Y, col);
                if (p.X > 0)
                    stack.Push(new Point(p.X - 1, p.Y));
                if (p.X < img.Width - 1)
                    stack.Push(new Point(p.X + 1, p.Y));
                if (p.Y > 0)
                    stack.Push(new Point(p.X, p.Y - 1));
                if (p.Y < img.Height - 1)
                    stack.Push(new Point(p.X, p.Y + 1));
            }
        }
        pictureBox1.Image = img;
    }
}
