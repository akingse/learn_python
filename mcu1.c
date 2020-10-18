//单片机控制直流电机程序
#include "reg52.h"
sbit BT1=P3^5;//定义输入
sbit BT2=P3^6;
sbit BT3=P3^7;
sbit MOTORL=P1^0;
sbit MOTORR=P1^1;
void motor_stop(){
    MOTORL=0; //前后定义不一致
    MOTORR=0;
}
void motor_forward(){
    MOTORL=1;
    MOTORR=0;
}
void motor_backard(){
    MOTORL=0;
    MOTORR=l;
}
void delay_m(unsigned char ms) { //自定义延迟函数
    unsigned char i,j;
    for(i=0;i<ms;i++){
        for(j=0;j<164;j++);
    }
}
main(){
    BT1=1;
    BT2=1;
    BT3=1;//复位
    while(1){
        if(BT1=0) {
            delay_m(10); 
            if(BT1==0){//手指左转 停下按键 手指归位
                motor_forward();                delay_m(3);
                motor_stop();                delay_m(1000);
                motor_backard();                delay_m(3);
            }
            if(BT2==0){
                delaym(10); 
                motor_backard();//手动复位
            }
        }

        if(BT3==0){
            delay_m(10);
            motor_stop();//手动停止
            
        }
    }
}


