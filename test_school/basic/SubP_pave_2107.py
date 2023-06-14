
# SubP_pave_2107.script
# original version
def SubP_pave(): #pave 6 pieces
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
	if (i<2): #when pave 2 3;
		offset=p[0,-(i+1)*(width+gap),0,0,0,0]
	else: #(i<5)  when pave 4 5 6;
		offset=p[-(width+gap),-(i-2)*(width+gap),0.002,0,0,0] #0.002 because robotarm unlevel;
	end
    # offset=p[0,0,-(i+1)*thickn,0,0,0] #palletizing

	point_pave_move=pose_trans(point_centre,offset) #posetrans tile first;
    point_pave = pose_trans(point_pave_move, delta_offset)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movel(pose_trans(point_pave,dropz),a=al,v=vl_erect) #pave,down
	set_standard_digital_out(4,False)
	sleep(0.5)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
end
# ----------------------------------------------
# version1
def SubP_pave_a():  # pave 6 pieces
	movej(point_turn, a=aj, v=vj_idle, r=r_wide)
	if (i < 2):  # when pave 2 3;
		offset = p[0, -(i+1)*(width+gap), 0, 0, 0, 0]
	else:  # (i<5)  when pave 4 5 6;
		offset = p[-(width+gap), -(i-2)*(width+gap), 0.002, 0, 0, 0]  # 0.002 because robotarm unlevel;
	end
    # offset=p[0,0,-(i+1)*thickn,0,0,0] #palletizing

	point_pave_move = pose_trans(point_centre, offset)  # posetrans tile first;
	movej(point_pave_move,a=aj,v=vj_idle,r=r_nar)  #pave,up
    thickn_a=0.009
    dropz = p[0, 0, 0.050-thickn_a, 0, 0, 0]
    point_pave1=pose_trans(point_pave_move,dropz)
	movel(point_pave1,a=al,v=vl_erect) #pave,down
    sleep(2)
    point_pave2 = pose_trans(point_pave1, delta_offset/2)
	movel(point_pave2 ,a=al,v=vl_erect) #pave,down
    sleep(2)
    point_pave3 = pose_trans(point_pave2, delta_offset/2)
	movel(point_pave3 ,a=al,v=vl_erect) #pave,down
    sleep(2)
    dropz = p[0, 0, thickn_a, 0, 0, 0]
    point_pave4=pose_trans(point_pave3,dropz)
    movel(point_pave4 ,a=al,v=vl_erect) #pave,down

	set_standard_digital_out(4,False)
	sleep(0.5)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
end



#------------------------------------------------
# 第一步 改铺贴顺序
global point_pave1 = p[0.990, 0.0, -0.135, pi, 0, 0] #point_above;
global point_pave1 = p[0.990, 0.600, -0.135, pi, 0, 0] #point_above;

	global point_scan=p[0.915,-0.130,scanh1,pi,0,0] #p1
	point_scan=p[0.715,-0.130,scanh1,pi,0,0] #p2
	point_scan=p[0.690,-0.100,scanh1,pi,0,0] #p3
	point_scan=p[0.690,0.100,scanh1,pi,0,0] #p4

 SubP_scan_datum():
	d2=0.6 #增加一个参数d2
	global point_scan=p[0.915,-0.130+d2,scanh1,pi,0,0] #p1
	point_scan=p[0.715,-0.130+d2,scanh1,pi,0,0] #p2
	point_scan=p[0.690,-0.100+d2,scanh1,pi,0,0] #p3
	point_scan=p[0.690,0.100+d2,scanh1,pi,0,0] #p4

SubP_pave()
	if (i<2):
		offset=p[0,(i+1)*(width+gap),0,0,0,0] # y值改成正号，下面也是
	else: #(i<5)
		offset=p[-(width+gap),(i-2)*(width+gap),0.002,0,0,0] #0.002 because robotarm unlevel;
	end

	global p_1=p_0
	point_scan=p[0.715,-0.130+d2,scanh1,pi,0,0] #p2
	movej(point_scan,a=aj,v=vj_idle)

#-------------------------------------------------
# version3
def SubP_pave_a():  #standstill
	movej(point_turn, a=aj, v=vj_idle, r=r_wide)
	if (i < 2):  # when pave 2 3;
		offset = p[0, (i+1)*(width+gap), 0, 0, 0, 0] #change the order
	else:  # (i<5)  when pave 4 5 6;
		offset = p[-(width+gap), (i-2)*(width+gap), 0, 0, 0, 0]
	end
    # offset=p[0,0,-(i+1)*thickn,0,0,0] #palletizing

	point_pave_move = pose_trans(point_centre, offset) #correct 1
	point_pave = pose_trans(point_pave_move, delta_offset)  #correct 2
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	point_paved = pose_trans(point_pave,dropz)
	devia = 0.010
	j=3
	while (j>=0):
		offdev= p[-j*devia,j*devia,-thickn,0,0,0] # deviate offset
		point_paven = pose_trans(point_paved,offdev)
		movel(point_paven,a=0.001,v=0.001)
    	sleep(2)
		j=j-1
	end
	offdown=p[0,0,thickn,0,0,0]
	movel(pose_trans(point_paved,offdown),a=0.001,v=0.001) # pave,down
	set_standard_digital_out(4,False)
	sleep(0.5)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
end

