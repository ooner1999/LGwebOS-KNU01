#include <dht.h> // DHT 라이브러리 호출
#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
dht DHT11;

int dhtSensor = 5;
int pulseSensor = A0;


void setup()
{
  Serial.begin(9600);
  mlx.begin();
}
 
void loop()
{

  int arr[10];
  int result = 0;
  int i = 0;
  int temp = 0;
  int b = analogRead(pulseSensor);
  int readData = DHT11.read11(dhtSensor);
  int t = DHT11.temperature; // 습도값을 h에 저장
  int h = DHT11.humidity; // 온도값을 t에 저장
  double c = mlx.readObjectTempC();
  
  if(b == 0)
  {
      for(int i=0; i<3; i++){
        arr[i] = map(analogRead(pulseSensor), 0, 500, 0, 130);
        delay(500);
        temp += arr[i];
      }

      result = temp/3;

      
      if(result != 0)
      {
        b = result;
        Serial.print("H:"); // 문자열 출력
        Serial.print(h); // 습도값 출력
        Serial.print("T:");
        Serial.print(t); // 온도값 출력
        Serial.print("B:");//심박수 출력
        Serial.print(b);
        Serial.print("C:");
        Serial.print(c+3);
        Serial.println("");
      }

  }

 }
