#include "DEV_Config.h"
#include "TCS34725.h"
RGB rgb,RGB888;
UWORD   RGB565=0;

void setup() {
  Config_Init();
  if(TCS34725_Init() != 0){
      Serial.print("TCS34725 initialization error!!\r\n");
      return 0; 
  } 
  Serial.print("TCS34725 initialization success!!\r\n");

 

}

void loop() {
  rgb=TCS34725_Get_RGBData();
  RGB888=TCS34725_GetRGB888(rgb);
  RGB565=TCS34725_GetRGB565(rgb);
  Serial.print("RGB888 :R=");
  Serial.print(RGB888.R);
  Serial.print(" G=");
  Serial.print(RGB888.G);
   Serial.print(" B=");
  Serial.print(RGB888.B);
  Serial.print("\r\n");


  Serial.print("RGB565= 0x");
  Serial.println((RGB565), HEX); 
  if(TCS34725_GetLux_Interrupt(0xff00, 0x00ff) == 1){
      Serial.print("Lux_Interrupt = 1\r\n");
  }else{
      Serial.print("Lux_Interrupt = 0\r\n");
  }
  Serial.print("\r\n");
  DEV_Delay_ms(1000);
}
