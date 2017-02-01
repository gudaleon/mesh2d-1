import math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        else:
            return 0.0

    def __iter__(self):
        return iter([self.x, self.y])

    def __str__(self):
        return "{0},{1}".format(self.x, self.y)

    def __add__(self, right_operand):
        return Vector2(self.x + right_operand.x, self.y + right_operand.y)

    def __sub__(self, right_operand):
        return Vector2(self.x - right_operand.x, self.y - right_operand.y)


    # scalar mul with scalar on the right
    def __mul__(self, right_scalar):
        return Vector2(self.x * right_scalar, self.y * right_scalar)


    # scalar division
    def __div__(self, right_operand):
        return Vector2(self.x / right_operand, self.y / right_operand)


    # scalar mul with scalar on the left
    def __rmul__(self, left_scalar):
        return Vector2(self.x * left_scalar, self.y * left_scalar)


    # equality
    def __eq__(self, right_operand):
        return self.x == right_operand.x and self.y == right_operand.y


    # inequality
    def __ne__(self, right_operand):
        return self.x != right_operand.x or self.y != right_operand.y


    def length(self):
        return math.sqrt(self.dot_product(self))


    def snap_to(self, other):
        self.x = other.x
        self.y = other.y


    @staticmethod
    def cross(v1, v2):
        return v1.x * v2.y - v2.x * v1.y

    @staticmethod
    def double_signed_area(v1, v2, v3):
        return Vector2.cross(v2 - v1, v3 - v1)


    @staticmethod
    def are_points_ccw(v1, v2, v3):
        return Vector2.double_signed_area(v1, v2, v3) > 0


    def dot_product(self, other):
        return self.x * other.x + self.y * other.y


    @staticmethod
    def point_inside(v0, v1, v2, v3):
        """
        Returns True iff v0 is inside the [v1, v2, v3] triangle
        """
        triangle_ccw = Vector2.are_points_ccw(v1, v2, v3)
        return (Vector2.are_points_ccw(v0, v1, v2) == triangle_ccw) and \
               (Vector2.are_points_ccw(v0, v2, v3) == triangle_ccw) and \
               (Vector2.are_points_ccw(v0, v3, v1) == triangle_ccw)

    @staticmethod
    def distance(v0, v1):
        dx = v0.x - v1.x
        dy = v0.y - v1.y
        return math.sqrt(dx*dx + dy*dy)


    @staticmethod
    def project_to_line(vert, line1, line2):
        # if line1 == line2:
        #   raise ZeroSegmentError("Line is defined by coincident points", [line1, line2])

        line_span = line2 - line1
        coef = (vert - line1).dot_product(line_span) / (line_span.dot_product(line_span))
        return line1 + (line_span * coef)

    @staticmethod
    def vertex_to_line_dist(vert, line1, line2):
        proj = Vector2.project_to_line(vert, line1, line2)
        return Vector2.distance(proj, vert)


    @staticmethod
    def angle(vect1, vect2):
        double_area = Vector2.double_signed_area(Vector2(0, 0), vect1, vect2)
        cos_angle = vect1.dot_product(vect2) / (vect1.length() * vect2.length())
        return math.acos(cos_angle)


    @staticmethod
    def mul_mtx(matrix, vector):
        if len(matrix) != 4:
            raise RuntimeError("Matrix must be 2x2")
        x = matrix[0]*vector.x + matrix[1]*vector.y
        y = matrix[2]*vector.x + matrix[3]*vector.y
        return Vector2(x, y)


    @staticmethod
    def vertex_to_segment_dist(vert, seg1, seg2):
        proj_point = Vector2.project_to_line(vert, seg1, seg2)
        if Vector2.point_between(proj_point, seg1, seg2):
            dist = Vector2.distance(proj_point, vert)

        else:
            dist1 = Vector2.distance(seg1, vert)
            dist2 = Vector2.distance(seg2, vert)
            dist = min(dist1, dist2)
            proj_point = seg1 if dist1 < dist2 else seg2

        return dist, proj_point



    @staticmethod
    def point_between(vert, vert1, vert2):
        '''
        Tells whether vert is between vert1 and vert2.
        Assumes they are on the same straight line.
        If vert == vert1 or vert == vert2, returns False.
        '''
        if vert1.x == vert2.x:
            ymin = min(vert1.y, vert2.y)
            ymax = max(vert1.y, vert2.y)
            return vert.y > ymin and vert.y < ymax
        else:
            xmin = min(vert1.x, vert2.x)
            xmax = max(vert1.x, vert2.x)
            return vert.x > xmin and vert.x < xmax



    @staticmethod
    def point_between_inclusive(vert, vert1, vert2):
        '''
        Tells whether vert is between vert1 and vert2.
        Assumes they are on the same straight line.
        If vert == vert1 or vert == vert2, returns True.
        '''
        if vert1.x == vert2.x:
            ymin = min(vert1.y, vert2.y)
            ymax = max(vert1.y, vert2.y)
            return vert.y >= ymin and vert.y <= ymax
        else:
            xmin = min(vert1.x, vert2.x)
            xmax = max(vert1.x, vert2.x)
            return vert.x >= xmin and vert.x <= xmax




    @staticmethod
    def _vertex_on_ray(vert, ray_tip, ray_target):
        return Vector2.point_between_inclusive(vert, ray_tip, ray_target) or \
        Vector2.point_between_inclusive(ray_target, ray_tip, vert)

                

    @staticmethod
    def segment_crosses_ray(seg1, seg2, ray1, ray2):
        '''
        Returns True if ray [ray1, ray2> intersects segment [seg1, seg2].
        Intersection at segment endpoints counts.
        Intersection at the tip of the ray counts.
        If segment and ray overlap in more than one point, returns False.
        '''

        # check if ray is undefined
        if ray1 == ray2:
            raise ValueError("Ray points cannot be the same")

        sarea_s1 = Vector2.double_signed_area(ray1, ray2, seg1)
        sarea_s2 = Vector2.double_signed_area(ray1, ray2, seg2)


        # seg1 on ray axis
        if sarea_s1 == 0:
            # seg2 also on ray axis
            if sarea_s2 == 0:

                '''
                only True case is when they overlap in
                exactly one point - the tip of the ray
                '''
                if seg1 == ray1 and \
                    Vector2.point_between_inclusive(ray1, seg2, ray2):
                    return True

                if seg2 == ray1 and \
                    Vector.point_between_inclusive(ray1, seg1, ray2):
                    return True

                # in other cases they either overlap too much or not at all
                return False

            # seg1 on ray axis, seg2 is not
            else:
                return Vector2._vertex_on_ray(seg1, ray1, ray2)


        # seg1 not on ray axis    
        else:
            # if seg2 on ray axis
            if sarea_s2 == 0:
                return Vector2._vertex_on_ray(seg2, ray1, ray2)

            # if neither seg1 nor seg2 are on ray axis
            else:
                s1_ccw = sarea_s1 > 0.
                s2_ccw = sarea_s2 > 0.
                # if seg1 and seg2 are on different sides of the ray:
                if s1_ccw != s2_ccw:
                    sarea_r1 = Vector2.double_signed_area(seg1, seg2, ray1)
                    sarea_r2 = Vector2.double_signed_area(seg1, seg2, ray2)


                    # if ray tip lies on the segment axis
                    if sarea_r1 == 0.:
                        # if ray tip lies on the segment, intersection is true,
                        # else false
                        return Vector2.point_between_inclusive(ray1, seg1, seg2)

                    # if ray tagret lies on segment axis:
                    if sarea_r2 == 0.:
                        # if ray target lies on the segment, intersection is true,
                        # else false
                        return Vector2.point_between_inclusive(ray2, seg1, seg2)


                    # now we ruled out all edge cases
                    r1_ccw = sarea_r1 > 0.
                    r2_ccw = sarea_r2 > 0.

                    # if r1 and r2 are on different sides of segment:
                    if r1_ccw != r2_ccw:
                        return True
                    # if r1 and r2 are on the same side of segment:
                    else:
                        ray1_dst = Vector2.vertex_to_line_dist(ray1, seg1, seg2)
                        ray2_dst = Vector2.vertex_to_line_dist(ray2, seg1, seg2)
                        # if r1 is further than r2, intersection is true
                        return ray1_dst >= ray2_dst

                # seg1 and seg2 are on the same side of the ray:
                else:
                    return False




    # @staticmethod
    # def segment_crosses_ray(seg1, seg2, ray1, ray2):
    #     '''
    #     Returns True if ray [ray1, ray2> intersects segment [seg1, seg2]
    #     '''

    #     # first check some edge cases
    #     # if seg1 == ray1 or seg2 == ray1:
    #     #   return True

    #     s1_left = Vector2.are_points_ccw(ray1, ray2, seg1)
    #     s2_left = Vector2.are_points_ccw(ray1, ray2, seg2)
    #     # if s1 and s2 are on different sides of the ray:
    #     if s1_left != s2_left:
    #         r1_left = Vector2.are_points_ccw(seg1, seg2, ray1)
    #         r2_left = Vector2.are_points_ccw(seg1, seg2, ray2)

    #         # if r1 and r2 are on different sides of segment:
    #         if r1_left != r2_left:
    #             return True
    #         # if r1 and r2 are on the same side of segment:
    #         else:
    #             ray1_dst = Vector2.vertex_to_line_dist(ray1, seg1, seg2)
    #             ray2_dst = Vector2.vertex_to_line_dist(ray2, seg1, seg2)
    #             # if r1 is further than r2, intersection is true
    #             if ray1_dst >= ray2_dst:
    #                 return True
    #             else:
    #                 return False
    #     else:
    #         return False

    

    @staticmethod
    def where_segment_crosses_ray(seg1, seg2, ray1, ray2):
        if not Vector2.segment_crosses_ray(seg1, seg2, ray1, ray2):
            return None
        # now we can assume they intersect:

        # if ray is vertical:
        if ray2.x - ray1.x == 0:
            seg_slope = (seg2.y - seg1.y) / (seg2.x - seg1.x)
            int_x = ray1.x
            int_y = seg1.y + (int_x - seg1.x) * seg_slope
            return Vector2(int_x, int_y)

        # if segment is vertical:
        elif seg2.x == seg1.x:
            ray_slope = (ray2.y - ray1.y) / (ray2.x - ray1.x)
            int_x = seg1.x
            int_y = ray1.y + (int_x - ray1.x) * ray_slope
            return Vector2(int_x, int_y)

        # if none of them is vertical:
        else:
            ray_slope = (ray2.y - ray1.y) / (ray2.x - ray1.x)
            seg_slope = (seg2.y - seg1.y) / (seg2.x - seg1.x)

            int_x = (ray1.y - seg1.y + seg1.x * seg_slope - ray1.x * ray_slope) / (seg_slope - ray_slope)
            int_y = ray1.y + (int_x - ray1.x) * ray_slope

            return Vector2(int_x, int_y)



class ZeroSegmentError(Exception):
    def __init__(self, message, segment):
        self._mes = message
        self._seg = segment

    def message(self):
        return self._mes

    def segment(self):
        return self._seg