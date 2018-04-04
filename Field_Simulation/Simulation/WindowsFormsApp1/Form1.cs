using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        Mutex cleanM = new Mutex();
        List<int[]> toClean = new List<int[]>();
        int vertical = 0;
        const int CIRCLE_TIME = 1 * 60 ;
        const int FIELD_SIZE = 50;
        Bitmap bitmap;
        DateTime time;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            time = DateTime.Now;
            this.bitmap = new Bitmap(pictureBox1.Width, pictureBox1.Height);
            pictureBox1.Image = this.bitmap;
            for(int i=0;i<this.bitmap.Width;i++)
            {
                for(int j=0;j<this.bitmap.Height;j++)
                {
                    this.bitmap.SetPixel(i, j, Color.White);
                }
            }
            Thread t = new Thread(() =>
            {
                try
                {
                    while (true)
                    {
                        //removes older vectors
                        Clean();
                        double angle = 360 * get_ratio();
                        angle = degrees_to_radians(angle);
                        int[] arr = circular_field(angle);
                        Invoke((MethodInvoker)delegate () { label1.Text = arr[0] + ":" + arr[1]; });
                        arr[1] = -arr[1];
                        Point vector = new Point(arr);
                        int[] zero = { bitmap.Width / 2, bitmap.Height / 2 };
                        int[] circ = { (int)(Math.Sin(angle) * 100)+bitmap.Width/2, -(int)(Math.Cos(angle) * 100)+bitmap.Height/2};
                        
                        //Printing the vertical vector to the circle
                        Invoke((MethodInvoker)delegate () { Line(circ,(vector+new Point(circ)).coordinates, 2,Color.Blue); });
                        Invoke((MethodInvoker)delegate () { pictureBox1.Image = this.bitmap; });

                        //Printing the circle
                        
                        Invoke((MethodInvoker)delegate () { draw_rect(circ, 2, Color.Black); });
                        Thread.Sleep(100);
                        }
                    }
                    catch(Exception exception) {
                        MessageBox.Show(exception.Message);
                    }
            });
            t.Start();
        }
        
        public double get_ratio()
        {
            DateTime time = DateTime.Now;
            TimeSpan t = time - this.time;
            return (t.TotalSeconds%CIRCLE_TIME) / CIRCLE_TIME;

        }
        /// <summary>
        /// Returns 2D vector of Circular Magnetic Field
        /// </summary>
        /// <param name="angle">The angle of the object relative to the path(degrees)</param>
        /// <returns>integer array that represents the vector of the field for the specified angle</returns>
        public int[] circular_field(double angle)
        {
            double a = Math.Sin(angle);
            double b = Math.Cos(angle);
            double x, y;
            if(b!=0)
            {
                int sign = (int)(b / Math.Abs(b));
                x = 1 * sign;
                y = -a / b * sign;
                double length = Math.Sqrt(x * x + y * y);
                x = x / length;
                y = y / length;
                y = y * FIELD_SIZE;
                x = x * FIELD_SIZE;
            }
            else
            {
                x = 0;
                y = -a;
            }
            int[] arr = { (int)Math.Round(x), (int)Math.Round(y) };
            return arr;

        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="angle"></param>
        /// <returns></returns>
        public int[] DePolarField(double angle)
        {
            //TODO : fix function to work
            return circular_field(angle * 2);
        }
        public double degrees_to_radians(double degrees)
        {
            return degrees*Math.PI/180;
        }
        //cleans all points from the clean list
        public void Clean()
        {
            cleanM.WaitOne();
            foreach(int[] pos in toClean)
            {
                bitmap.SetPixel(pos[0], pos[1], Color.White);
            }
            cleanM.ReleaseMutex();
        }
        public void draw_circle(int thickness)
        {

        }
        public void draw_rect(int[] location,int size,Color c ,bool clean = false)
        {
            for(int i=location[0]-size;i<location[0]+size;i++)
            {
                for(int j=location[1]-size;j<location[1]+size;j++)
                {
                    this.bitmap.SetPixel(i, j,c);
                    if(clean)
                    {
                        int[] pos = { i, j };
                        cleanM.WaitOne();
                        toClean.Add(pos);
                        cleanM.ReleaseMutex();
                    }

                }
            }

        }
        
        public void Line(int[] p1,int[] p2,int size,Color c)
        {
            int[] start = { p1[0], p1[1] };
            int[] end = { p2[0], p2[1] };
            if (end[0] == start[0])
            {
                for(int i=start[1];i<=end[1];i++)
                {
                    int[] location = { start[0], i };
                    draw_rect(location, 2, c, true);
                }
            }
            else 
            {
                if (start[0] > end[0])
                {
                    int[] temp = { start[0], start[1] };
                    start[0] = end[0];
                    start[1] = end[1];
                    end = temp;
                }
                float slowpe = ((float)(end[1] - start[1])) / ((float)(end[0] - start[0]));
                for(float i=start[0];i<=end[0];i+=0.1f)
                {
                    int[] location = { (int)Math.Round(i), start[1] + (int)(slowpe * (i-start[0])) };
                    draw_rect(location, 2, c, true);
                }
            }
        }
    }
}
