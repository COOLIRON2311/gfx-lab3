using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lab3
{
    public partial class Form1 : Form
    {
        enum Mode { Free, Line };

        Mode mode = Mode.Free;

        Point firstLineP;
        Point secondLineP;

        Color col;
        Bitmap img;
        Bitmap tempImg;
        Graphics g;
        Pen pen;
        bool mouseDown;
        int x, y;
        public Form1()
        {
            col = Color.Black;
            InitializeComponent();
            radioButton1.Checked = true;
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
            if (mode == Mode.Free)
            {
                if (e.Button == MouseButtons.Right)
                {
                    LinearFloodFillWithImage(e.X, e.Y);
                    // img.Save("image.png");
                }
            }
            else if (mode == Mode.Line)
            {
                if (e.Button == MouseButtons.Left)
                {
                    firstLineP = e.Location;
                }
                else
                {
                    secondLineP = e.Location;
                    DrawLineWu(firstLineP, secondLineP);
                }
            }
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {

            if (mode == Mode.Free)
            {
                if (e.KeyCode == Keys.Escape)
                {
                    img = new Bitmap(Width, Height);
                    g = Graphics.FromImage(img);
                    pictureBox1.Image = img;
                }
            }
        }

        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (mode == Mode.Free)
            {
                if (mouseDown && e.Button == MouseButtons.Left)
                {
                    g.DrawLine(pen, new Point(x, y), e.Location);
                    x = e.X;
                    y = e.Y;
                    pictureBox1.Image = img;
                }
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

        private void LinearFloodFill(int x, int y)
        {
            Color targetColor = Color.FromArgb(0, 0, 0, 0);
            if (targetColor == col)
                return;
            Stack<Point> stack = new Stack<Point>();
            stack.Push(new Point(x, y));

            while (stack.Count > 0)
            {
                Point p = stack.Pop();

                if (img.GetPixel(p.X, p.Y) != targetColor)
                    continue;

                int leftBorder = p.X;
                int rightBorder = p.X;

                for (int i = p.X; i < img.Width; i++)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    rightBorder = i;

                    img.SetPixel(i, p.Y, col);
                }

                for (int i = p.X - 1; i >= 0; i--)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    leftBorder = i;

                    img.SetPixel(i, p.Y, col);
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y + 1 < img.Height)
                        stack.Push(new Point(i, p.Y + 1));
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y - 1 > 0)
                        stack.Push(new Point(i, p.Y - 1));
                }

            }
                pictureBox1.Image = img;
        }
        private void LinearFloodFillWithImage(int x, int y)
        {
            Color targetColor = Color.FromArgb(0, 0, 0, 0);
            /*if (targetColor == col)
                return;*/
            Stack<Point> stack = new Stack<Point>();
            stack.Push(new Point(x, y));

            while (stack.Count > 0)
            {
                Point p = stack.Pop();

                if (img.GetPixel(p.X, p.Y) != targetColor)
                    continue;

                int leftBorder = p.X;
                int rightBorder = p.X;

                for (int i = p.X,j=0; i < img.Width; i++,j++)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    rightBorder = i;

                    img.SetPixel(i, p.Y, tempImg.GetPixel(Math.Abs(x-i+tempImg.Width/2)%tempImg.Width, Math.Abs(p.Y-y+tempImg.Height/2)%tempImg.Height));
                }

                for (int i = p.X - 1,j=0; i >= 0; i--,j++)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    leftBorder = i;

                    img.SetPixel(i, p.Y, tempImg.GetPixel(Math.Abs(x-i+tempImg.Width/2) % tempImg.Width, Math.Abs(p.Y-y+tempImg.Height/2) % tempImg.Height));
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y + 1 < img.Height)
                        stack.Push(new Point(i, p.Y + 1));
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y - 1 > 0)
                        stack.Push(new Point(i, p.Y - 1));
                }

            }
            pictureBox1.Image = img;
        }

        private void DrawLineBresenham(Point a, Point b)
        {
            if(a.X>b.X)
            {
                Point c = a;
                a = b;
                b = c;
            }

            int dx = b.X - a.X;
            int dy = b.Y - a.Y;

            float gradient = 1;

            if (dy != 0)
            {
                gradient = Math.Abs((float)dy / dx);
            }

            int curX = a.X;
            int curY = a.Y;

            float d = 2 * dy - dx;

            while (curX < b.X )
            {

                if (gradient <= 1)
                {
                    if (d >= 0)
                    {
                        curY=curY + Math.Sign(dy);
                        d = d + 2 * (Math.Abs(dy) - dx);
                    }
                    else
                    {
                        d = d + 2 * Math.Abs(dy);
                    }

                    curX++;
                }
                else {
                    if (d >= 0)
                    {
                        curX++;
                        d = d + 2 * (dx - Math.Abs(dy));
                    }
                    else
                    {
                        d = d + 2 * dx;
                    }

                    curY = curY + Math.Sign(dy);
                }

                img.SetPixel(curX,curY, col);
            }

            pictureBox1.Image = img;
        }

        private void DrawLineWu(Point a, Point b)
        {
            if (a.X > b.X)
            {
                Point c = a;
                a = b;
                b = c;
            }

            float dx = b.X - a.X;
            float dy = b.Y - a.Y;

            float gradient = dy / dx;

            float y = a.Y + gradient;


            if (Math.Abs(gradient) < 1)
            {
                if (a.X > b.X)
                {
                    Point c = a;
                    a = b;
                    b = c;
                }

                for (int i = a.X + 1; i < b.X - 1; i++)
                {
                    float dif = (y - ((int)y)) * 256;
                    img.SetPixel(i, (int)y, Color.FromArgb(255 - (int)(dif), col.R, col.G, col.B));
                    img.SetPixel(i, (int)y + 1, Color.FromArgb((int)(dif), col.R, col.G, col.B));
                    y += gradient;
                }
            }
            else
            {
                if (a.Y > b.Y)
                {
                    Point c = a;
                    a = b;
                    b = c;
                }

                float gradient2 = dx / dy;
                float x = a.X + gradient2;

                for (int i = a.Y + 1; i < b.Y - 1; i++)
                {
                    float dif = (x - ((int)x)) * 256;
                    img.SetPixel((int)x,i, Color.FromArgb(255 - (int)(dif), col.R, col.G, col.B));
                    img.SetPixel((int)x + 1,i, Color.FromArgb((int)(dif), col.R, col.G, col.B));
                    x += gradient2;
                }
            }



            pictureBox1.Image = img;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog();
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                col = colorDialog.Color;
                pen = new Pen(col, 5);
            }
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
                mode = Mode.Free;
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton2.Checked)
                mode = Mode.Line;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog dlg = new OpenFileDialog())
            {
                dlg.Title = "Open Image";
                dlg.Filter = "bmp files (*.bmp)|*.bmp";
                dlg.Filter += "|jpg files (*.jpg)|*.jpg";
                dlg.Filter += "|png files (*.png)|*.png";

                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    tempImg = new Bitmap(dlg.FileName);
                }
            }
        }
    }
}
