using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WindowsFormsApp1
{
    class Point
    {
        public int[] coordinates { get; private set; }
        public Point(int[] arr)
        {
            this.coordinates = new int[2];
            this.coordinates[0] = arr[0];
            this.coordinates[1] = arr[1];
        }
        /// <summary>
        /// Calculates the distance between the point and the other point
        /// </summary>
        /// <param name="other">The second point</param>
        /// <returns>The distance between the points</returns>
        public double distance(Point other)
        {
            int[] x = { this.coordinates[0] ,other.coordinates[0] };
            int[] y = { this.coordinates[1], other.coordinates[1] };
            return Math.Sqrt(Math.Pow(x[0] - x[1], 2) + Math.Pow(y[0] - y[1], 2));
        }
        public static Point operator +(Point first ,Point second)
        {
            int[] arr = { first.coordinates[0] + second.coordinates[0], first.coordinates[1] + second.coordinates[1] };
            return new Point(arr);
        }
        public static Point operator-(Point first ,Point second)
        {
            int[] arr = { first.coordinates[0] - second.coordinates[0], first.coordinates[1] - second.coordinates[1] };
            return new Point(arr);
        }
    }
}
