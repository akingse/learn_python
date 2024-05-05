
import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
# 测试用例程序，仅供测试使用

# 两截面，引导线，原生写法
secBot = Section(Vec3(-500, -500, 0), Vec3(500, -500, 0),
                 Vec3(500, 500, 0), Vec3(-500, 500, 0))
secTop = transz(1200)*scale(0.6)*secBot

guideLine = [[Segment(Vec3(-500, -500, 0), Vec3(-300, -300, 1200)),
              Segment(Vec3(500, -500, 0), Vec3(300, -300, 1200)),
              Segment(Vec3(500, 500, 0), Vec3(300, 300, 1200)),
              Segment(Vec3(-500, 500, 0), Vec3(-300, 300, 1200))]]
lofted = Lofted(secBot, secTop, guideLine)
# create_geometry(transx(-2000)*lofted.colorBlue())



# 单层引导线
guideLine = [Line(Vec3(-500, -500, 0), Vec3(-300, -300, 1200)),
             Line(Vec3(500, -500, 0), Vec3(300, -300, 1200)),
             Line(Vec3(500, 500, 0), Vec3(300, 300, 1200)),
             Line(Vec3(-500, 500, 0), Vec3(-300, 300, 1200))]  # Segment Line均可
lofted = Lofted(secBot, secTop, guideLine)
# create_geometry(transy(2000)*lofted)

r=100
h=100
n=25

secBot=[]
guideLine=[]
for i in range(n):
    pnt=scale(1,1)*Vec3(r*sin(i/n*2*pi),r*cos(i/n*2*pi))
    secBot.append(pnt)
    guideLine.append(Segment(pnt,transz(h)*pnt))

# secBot.append(secBot[0])
# guideLine.append(guideLine[0])

secBot=Section(secBot)
secTop=transz(h)*secBot



lofted = Lofted(secBot, secTop, guideLine)
# create_geometry(lofted)

# -----------------------------------------------------------------------------------
from msilib.schema import ControlCondition
from pyp3d import *
import pyp3d as p3d
class 站台梁板(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件类型'] = Attr('梁板',obvious=True,readonly=True,group='构件分类')
        self['构件名称'] = Attr('高铁站台雨棚-梁板（弧段）',obvious=True,readonly=True,group='构件分类')

        self['板底标高'] = Attr(0, obvious = True, group = "定位信息")  #0（可变参数）
        self['1端-距中心线'] = Attr(5000, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        self['1/2端-距中心线'] = Attr(5400, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        self['2/3端-距中心线'] = Attr(5600, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        self['3端-距中心线'] = Attr(5700, obvious = True, group = "板轮廓尺寸")  #（可变参数）

        self['1弧段长度'] = Attr(12000, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        self['1段弧度'] = Attr(12400, obvious = True,readonly=True, group = "板轮廓尺寸")  #（可变参数）
        self['2弧段长度'] = Attr(12000, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        self['2段弧度'] = Attr(12400, obvious = True,readonly=True, group = "板轮廓尺寸")  #（可变参数）
        self['3弧段长度'] = Attr(12000, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        self['3段弧度'] = Attr(12400, obvious = True,readonly=True, group = "板轮廓尺寸")  #（可变参数）

        # self['板长度'] = Attr(12000, obvious = True, group = "板轮廓尺寸")  #（可变参数）
        # self['板宽度'] = Attr(5400, obvious = True, group = "板轮廓尺寸")  #（可变参数））

        self['内侧板厚'] = Attr(120, obvious = True, group = "梁板尺寸（内侧）")  #（可变参数）
        self['梁板弧半径（内侧）'] = Attr(940, obvious = True, group = "梁板尺寸（内侧）")  #（可变参数））

        self['外侧板厚'] = Attr(150, obvious = True, group = "梁板尺寸（外侧）")  #（可变参数））
        self['外侧板顶坡度线宽度'] = Attr(2100, obvious = True, group = "梁板尺寸（外侧）")  #（可变参数））
        self['外侧板高度'] = Attr(300, obvious = True, group = "梁板尺寸（外侧）")  #（可变参数））
        self['外侧板坡度'] = Attr(  obvious = True, readonly=True, group = "梁板尺寸（外侧）")    #需要依据【外侧板顶坡度线宽度】、【外侧板高度】+【内侧板厚】确定此参数，不需要修改，仅预览显示在属性栏，供用户参考       
        self['反梁高度'] = Attr(450, obvious = True, group = "梁板尺寸（外侧）")  #（可变参数））       
        self['反梁宽度'] = Attr(300, obvious = True, group = "梁板尺寸（外侧）")  #（可变参数））       
        self['梁板弧半径（外侧）'] = Attr(1200, obvious = True, group = "梁板尺寸（外侧）")  #（可变参数））

        self['柱定位线偏移'] = Attr(3000, obvious = True, group = "梁板尺寸（柱连接位置）")  #（可变参数））原先1400
        self['梁柱底连接宽度'] = Attr(730, obvious = True, group = "梁板尺寸（柱连接位置）")  #（可变参数））
        
        self['过水孔宽度'] = Attr(400, obvious = True, group = "过水孔")  #（可变参数））
        self['过水孔间板厚度'] = Attr(140, obvious = True, group = "过水孔")  #（可变参数））
        self['过水孔高度（上）'] = Attr(270, obvious = True, group = "过水孔")  #（可变参数））
        self['过水孔高度（下）'] = Attr(500, obvious = True, group = "过水孔")  #（可变参数））
        self['材质'] = Attr('', obvious = True, material = True, group="材质")    #灰色（下拉选择，支持选择材质库中的项）
        self['小圆孤角度'] = Attr(69, obvious = True, group = '其它')
        # self['外侧板坡度'] = Attr(0.02, obvious = True, group = '梁板信息同步')
        # self['梁柱底连接宽度'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        # self['梁板弧半径（外侧）'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        # self['梁板弧半径（内侧）'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        # self['板底标高'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        # self['外侧板坡度'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        # self['过水孔宽度'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        # self['过水孔高度（下）'] = Attr( obvious = True,readonly=True, group = "柱信息同步")  #置灰不可修改，显示参考上方参数值
        self['站台梁板'] = Attr(None, show=True)
        self.replace()
    @export
    

    
    def replace(self):
        
        # L = self['板长度']
        # W = self['板宽度']
        BB_H = self['板底标高']
        thick_out = self['外侧板厚']
        thick_innerBoard = self['内侧板厚']
        wide_OutBoard = self['外侧板顶坡度线宽度']
        high_out = self['外侧板高度']

        hole_up = self['过水孔高度（上）']
        hole_down = self['过水孔高度（下）']
        hole_wide = self['过水孔宽度']
        hole_thick = self['过水孔间板厚度']
        beam_high = self['反梁高度']
        beam_wide = self['反梁宽度']
        LB_LN = self['梁板弧半径（外侧）']
        LB_RN = self['梁板弧半径（内侧）']
        CPLO = self['柱定位线偏移']
        LZL_W  = self['梁柱底连接宽度']
        a = self['小圆孤角度']/180*pi  #69°转化成狐度     
  
        #计算坡度
        L_line = sqrt(pow(wide_OutBoard, 2)+pow((high_out-thick_innerBoard), 2))
        #print(L_line)
        # #
        b = wide_OutBoard
        c = L_line
        self['外侧板坡度'] = math.degrees(math.acos(b / c))
        #print("外侧板坡度1:",self['外侧板坡度'])  

        bpdou =0.02 #self['外侧板弧度']0.02弧度

        #固定小夹角为9°，小正方形边长为25
        y_cube = 25/tan(math.radians(9))
        print(y_cube)
        LB_H = -(hole_up-thick_innerBoard+hole_down+hole_thick)
        # 描述截面
        cross_beam1 = trans(-(self['1端-距中心线']-CPLO),0,0)*Section(
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,thick_innerBoard),
                            Vec2(self['1端-距中心线']-CPLO,thick_innerBoard),
                            Vec2(self['1端-距中心线']-CPLO,0),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+(LB_RN+50)*sin(a),0),Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),LB_RN),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),Vec2(1/2*LZL_W,-(hole_up-thick_innerBoard+hole_down+hole_thick)),-50),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W,LB_H),Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),-50),  
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),Vec2(-1/2*LZL_W-50*sin(a)-LB_LN*sin(a)+LB_LN*sin(bpdou),LB_H+50-50*cos(a)-LB_LN*cos(a)+LB_LN*cos(bpdou)),LB_LN),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            arc_of_radius_points_2D(Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),Vec2(-CPLO,high_out-thick_innerBoard-y_cube+thick_innerBoard+250),-250),
                            Vec2(-CPLO,high_out+beam_high),
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high),       
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high-80),       
                            Vec2(-CPLO+beam_wide,high_out+beam_high-80),    
                            Vec2(-CPLO+beam_wide,high_out),                            
                            Vec2(-(CPLO-(wide_OutBoard+beam_wide)),thick_innerBoard),   
                            Vec2(-(hole_wide/2),thick_innerBoard),                            
                         
                          
                    
)
#         cross_beam1
        
        cross_beam2 = trans(-(self['1/2端-距中心线']-CPLO),0,-self['1弧段长度'])*Section(
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,thick_innerBoard),
                            Vec2(self['1/2端-距中心线']-CPLO,thick_innerBoard),
                            Vec2(self['1/2端-距中心线']-CPLO,0),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+(LB_RN+50)*sin(a),0),Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),LB_RN),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),Vec2(1/2*LZL_W,-(hole_up-thick_innerBoard+hole_down+hole_thick)),-50),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                           
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W,LB_H),Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),-50),  
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),Vec2(-1/2*LZL_W-50*sin(a)-LB_LN*sin(a)+LB_LN*sin(bpdou),LB_H+50-50*cos(a)-LB_LN*cos(a)+LB_LN*cos(bpdou)),LB_LN),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            arc_of_radius_points_2D(Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),Vec2(-CPLO,high_out-thick_innerBoard-y_cube+thick_innerBoard+250),-250),
                            Vec2(-CPLO,high_out+beam_high),
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high),       
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high-80),       
                            Vec2(-CPLO+beam_wide,high_out+beam_high-80),    
                            Vec2(-CPLO+beam_wide,high_out),                            
                            Vec2(-(CPLO-(wide_OutBoard+beam_wide)),thick_innerBoard),   
                            Vec2(-(hole_wide/2),thick_innerBoard),                            
                         
                           
                    
)
        cross_beam3 = trans(-(self['2/3端-距中心线']-CPLO),0,-self['1弧段长度']-self['2弧段长度'])*Section(
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,thick_innerBoard),
                            Vec2(self['2/3端-距中心线']-CPLO,thick_innerBoard),
                            Vec2(self['2/3端-距中心线']-CPLO,0),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+(LB_RN+50)*sin(a),0),Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),LB_RN),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),Vec2(1/2*LZL_W,-(hole_up-thick_innerBoard+hole_down+hole_thick)),-50),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W,LB_H),Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),-50),  
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),Vec2(-1/2*LZL_W-50*sin(a)-LB_LN*sin(a)+LB_LN*sin(bpdou),LB_H+50-50*cos(a)-LB_LN*cos(a)+LB_LN*cos(bpdou)),LB_LN),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            arc_of_radius_points_2D(Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),Vec2(-CPLO,high_out-thick_innerBoard-y_cube+thick_innerBoard+250),-250),
                            Vec2(-CPLO,high_out+beam_high),
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high),       
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high-80),       
                            Vec2(-CPLO+beam_wide,high_out+beam_high-80),    
                            Vec2(-CPLO+beam_wide,high_out),                            
                            Vec2(-(CPLO-(wide_OutBoard+beam_wide)),thick_innerBoard),   
                            Vec2(-(hole_wide/2),thick_innerBoard),                            
                         
                    
)
        
        cross_beam4 = trans(-(self['3端-距中心线']-CPLO),0,-self['1弧段长度']-self['2弧段长度']-self['3弧段长度'])*Section(
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard)),
                            Vec2(hole_wide/2,thick_innerBoard),
                            Vec2(self['3端-距中心线']-CPLO,thick_innerBoard),
                            Vec2(self['3端-距中心线']-CPLO,0),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+(LB_RN+50)*sin(a),0),Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),LB_RN),
                            arc_of_radius_points_2D(Vec2(1/2*LZL_W+50*sin(a),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a)),Vec2(1/2*LZL_W,-(hole_up-thick_innerBoard+hole_down+hole_thick)),-50),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            Vec2(hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_thick)),
                            Vec2(-hole_wide/2,-(hole_up-thick_innerBoard+hole_down+hole_thick)),
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W,LB_H),Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),-50),  
                            arc_of_radius_points_2D(Vec2(-1/2*LZL_W-50*sin(a),LB_H+50-50*cos(a)),Vec2(-1/2*LZL_W-50*sin(a)-LB_LN*sin(a)+LB_LN*sin(bpdou),LB_H+50-50*cos(a)-LB_LN*cos(a)+LB_LN*cos(bpdou)),LB_LN),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            Vec2(-(CPLO-beam_wide),high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard+25),
                            Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),
                            arc_of_radius_points_2D(Vec2(-(CPLO-beam_wide)-25,high_out-thick_innerBoard-y_cube+thick_innerBoard),Vec2(-CPLO,high_out-thick_innerBoard-y_cube+thick_innerBoard+250),-250),
                            Vec2(-CPLO,high_out+beam_high),
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high),       
                            Vec2(-CPLO+beam_wide+80,high_out+beam_high-80),       
                            Vec2(-CPLO+beam_wide,high_out+beam_high-80),    
                            Vec2(-CPLO+beam_wide,high_out),                            
                            Vec2(-(CPLO-(wide_OutBoard+beam_wide)),thick_innerBoard),   
                            Vec2(-(hole_wide/2),thick_innerBoard),                            
                         
                    
)
        guideLine1 = [
                        Segment(Vec3(-hole_wide/2-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard),0),Vec3(-hole_wide/2-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard),-self['1弧段长度'])),
                        Segment(Vec3(hole_wide/2-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard),0),Vec3(hole_wide/2-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard),-self['1弧段长度'])),
                        Segment(Vec3(hole_wide/2-(self['1端-距中心线']-CPLO),thick_innerBoard,0),Vec3(hole_wide/2-(self['1/2端-距中心线']-CPLO),thick_innerBoard,-self['1弧段长度'])),
                        Segment(Vec3(self['1端-距中心线']-CPLO-(self['1端-距中心线']-CPLO),thick_innerBoard,0),Vec3(self['1/2端-距中心线']-CPLO-(self['1/2端-距中心线']-CPLO),thick_innerBoard,-self['1弧段长度'])),
                        Segment(Vec3(self['1端-距中心线']-CPLO-(self['1端-距中心线']-CPLO),0,0),Vec3(self['1/2端-距中心线']-CPLO-(self['1/2端-距中心线']-CPLO),0,-self['1弧段长度'])),

                        Segment(Vec3(1/2*LZL_W+(LB_RN+50)*sin(a)-(self['1端-距中心线']-CPLO),0,0),Vec3(1/2*LZL_W+(LB_RN+50)*sin(a)-(self['1/2端-距中心线']-CPLO),0,-self['1弧段长度'])),
                        Segment(Vec3(1/2*LZL_W+50*sin(a)-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a),0),Vec3(1/2*LZL_W+50*sin(a)-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick)+50-50*cos(a),-self['1弧段长度'])),
                        Segment(Vec3(1/2*LZL_W-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick),0),Vec3(1/2*LZL_W-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick),-self['1弧段长度'])),#jia上的

                        Segment(Vec3(hole_wide/2-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick),0),Vec3(hole_wide/2-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick),-self['1弧段长度'])),
                        Segment(Vec3(hole_wide/2-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_thick),0),Vec3(hole_wide/2-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_thick),-self['1弧段长度'])),
                        Segment(Vec3(-hole_wide/2-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_thick),0),Vec3(-hole_wide/2-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_thick),-self['1弧段长度'])),
                        Segment(Vec3(-hole_wide/2-(self['1端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick),0),Vec3(-hole_wide/2-(self['1/2端-距中心线']-CPLO),-(hole_up-thick_innerBoard+hole_down+hole_thick),-self['1弧段长度'])),
                        
                        Segment(Vec3(-1/2*LZL_W-(self['1端-距中心线']-CPLO),LB_H,0),Vec3(-1/2*LZL_W-(self['1/2端-距中心线']-CPLO),LB_H,-self['1弧段长度'])),
                        Segment(Vec3(-1/2*LZL_W-50*sin(a)-(self['1端-距中心线']-CPLO),LB_H+50-50*cos(a),0),Vec3(-1/2*LZL_W-50*sin(a)-(self['1/2端-距中心线']-CPLO),LB_H+50-50*cos(a),-self['1弧段长度'])),
#2                      
                        Segment(Vec3(-(self['1端-距中心线']-CPLO)+(-1/2*LZL_W-50*sin(a)-LB_LN*sin(a)+LB_LN*sin(bpdou)),LB_H+50-50*cos(a)-LB_LN*cos(a)+LB_LN*cos(bpdou),0),Vec3(-(self['1/2端-距中心线']-CPLO)+(-1/2*LZL_W-50*sin(a)-LB_LN*sin(a)+LB_LN*sin(bpdou)),LB_H+50-50*cos(a)-LB_LN*cos(a)+LB_LN*cos(bpdou),-self['1弧段长度'])), #jia上的
                        Segment(Vec3(-(CPLO-beam_wide)-(self['1端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard,0),Vec3(-(CPLO-beam_wide)-(self['1/2端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard,-self['1弧段长度'])),
                        Segment(Vec3(-(CPLO-beam_wide)-(self['1端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard+25,0),Vec3(-(CPLO-beam_wide)-(self['1/2端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard+25,-self['1弧段长度'])),
                        Segment(Vec3(-(CPLO-beam_wide)-25-(self['1端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard+25,0),Vec3(-(CPLO-beam_wide)-25-(self['1/2端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard+25,-self['1弧段长度'])),
                        Segment(Vec3(-(CPLO-beam_wide)-25-(self['1端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard,0),Vec3(-(CPLO-beam_wide)-25-(self['1/2端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard,-self['1弧段长度'])),
                        Segment(Vec3(-CPLO-(self['1端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard+250,0),Vec3(-CPLO-(self['1/2端-距中心线']-CPLO),high_out-thick_innerBoard-y_cube+thick_innerBoard+250,-self['1弧段长度'])),

                        Segment(Vec3(-CPLO-(self['1端-距中心线']-CPLO),high_out+beam_high,0),Vec3(-CPLO-(self['1/2端-距中心线']-CPLO),high_out+beam_high,-self['1弧段长度'])),
                        Segment(Vec3(-CPLO+beam_wide+80-(self['1端-距中心线']-CPLO),high_out+beam_high,0),Vec3(-CPLO+beam_wide+80-(self['1/2端-距中心线']-CPLO),high_out+beam_high,-self['1弧段长度'])),
                        Segment(Vec3(-CPLO+beam_wide+80-(self['1端-距中心线']-CPLO),high_out+beam_high-80,0), Vec3(-CPLO+beam_wide+80-(self['1/2端-距中心线']-CPLO),high_out+beam_high-80,-self['1弧段长度'])),
                        Segment(Vec3(-CPLO+beam_wide-(self['1端-距中心线']-CPLO),high_out+beam_high-80,0),Vec3(-CPLO+beam_wide-(self['1/2端-距中心线']-CPLO),high_out+beam_high-80,-self['1弧段长度'])),
                        Segment(Vec3(-CPLO+beam_wide-(self['1端-距中心线']-CPLO),high_out,0),Vec3(-CPLO+beam_wide-(self['1/2端-距中心线']-CPLO),high_out,-self['1弧段长度'])),
                        
                        Segment(Vec3(-(CPLO-(wide_OutBoard+beam_wide))-(self['1端-距中心线']-CPLO),thick_innerBoard,0), Vec3(-(CPLO-(wide_OutBoard+beam_wide))-(self['1/2端-距中心线']-CPLO),thick_innerBoard,-self['1弧段长度'])),
                        Segment(Vec3(-(hole_wide/2)-(self['1端-距中心线']-CPLO),thick_innerBoard,0),Vec3(-(hole_wide/2)-(self['1/2端-距中心线']-CPLO),thick_innerBoard,-self['1弧段长度']))
                      ]
        
        loft1 = Lofted(cross_beam1,cross_beam2)
        loft1.showTest=True
        create_geometry(loft1)

        # loft1 = rotx(1/2*pi)*Loft(cross_beam1,cross_beam2,cross_beam3,cross_beam4)
        # loft1 = Combine(cross_beam1,cross_beam2,guideLine1)
        
                      
                      
#         cross_beam = trans(0,0,BB_H)*rotx(1/2*pi)*Sweep(cross_beam,Line(Vec3(0,0,0),Vec3(0,0,self['1段弧度']))).material(self['材质'])
#         Lofted 

        # self['站台梁板'] = loft1




if __name__ == "__main__":
    FinalGeometry = 站台梁板()
    place_to(FinalGeometry)


