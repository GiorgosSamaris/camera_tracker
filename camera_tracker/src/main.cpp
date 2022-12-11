#include <Arduino.h>
#include <Servo.h>
#include <Config.hpp>
#include "CircularQueue.hpp"

Servo yaw;
Servo pitch;
CircularQueue<uint8_t, 64> buffer(true);
char c;

void setup() 
{
  	Serial.begin(9600);
	yaw.attach(Motor::YAW_PWM_PIN, 500, 2500);
	pitch.attach(Motor::PITCH_PWM_PIN, 500, 2500);
	yaw.write(90);
	pitch.write(90);
	delay(3000);
}

void loop() 
{
//  for(int ang = 0; ang <= 180; ang++)
//	{
//		yaw.write(ang);
//		pitch.write((ang*2)/3);
//		delay(10);
//	}
//
//
//
//  	for(int ang = 180; ang >= 0; ang--)
//	{
//		yaw.write(ang);
//		pitch.write((ang*2)/3);
//		delay(10);
//	}
	while(Serial.available())
	{
		buffer.enqueue(Serial.read());
	}
	while(!buffer.isEmpty())
	{
		c = buffer.dequeue();
		if(c == '1')
			yaw.write(yaw.read()+1);
		else if(c == '2')
			pitch.write(pitch.read()+1);
		else if(c == '3')
			yaw.write(yaw.read()-1);
		else if(c == '4')
			pitch.write(pitch.read()-1);

	}

}