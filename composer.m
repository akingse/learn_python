//Code Composer Studio编程
//composer程序
#@AUTOEXEC
	//全局变量声明
	int location[4];
	int i;
	int a;

	##PROGRAM//使用位置
	location[0]=-4800;
	location[1]=4800;
	location[2]=-19200;
	location[3]=19200;

	if (UM!=5)  	//选取模式
		MO=0
	end

	if (MO==0)
		UM=5		
		MO=1		
	end

	il[3]=6
	il[2]=6
	OB[1]=1
	OB[2]=1	//关闭状态
	i=0;
	while(!IB[2]) 
		if (IB[3]==0)  //接受移动信号
			i=a
			OB[1]=0
			OB[2]=1	//锁定手指
			wait(250)
			a=i	
			Move(i)
			i=a+1
			OB[1]=0
			OB[2]=1	
			wait(250)
			a=a+1
			Move(i)
			a=a+1
		end
	end

	MO=0
	goto#@AUTOEXEC
return;//结束程序

//子程序
function int Err=Move(int index)
	global int location[4];//使用全局变量
	//局部变量
	int dest;
	Err=0;
 	if(index==12||index==13)//移动位置定义
		if(index%2==0)
			dest=location[2];
		else
			dest=location[3];
		end
	else 
		if(index%2==0)
			dest=location[0];
		else
			dest=location[1];
		end
	end
		
	try //走绝对位置
		SP=80000;	
		PR=dest;
		BG;		
	until(MS==1)
		OB[1]=1;
		OB[2]=0;
		wait(1000);//延时程序
	catch
		Err=prgerr(0);
	end
return;
