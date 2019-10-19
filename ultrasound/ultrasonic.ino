int trigpin = 13;
int echopin = 11;
float pingtime;   // Time required to hit the target and echo back
float speedofsound;
float distance = 0.13;

void setup() 
{  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(trigpin, OUTPUT);  
  pinMode(echopin, INPUT);   
  
}

void loop() 
{ 
  digitalWrite(trigpin, LOW);
  delayMicroseconds(2000);  // Just give chance for signal to settle down
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);  // Just give chance for signal to settle down
  digitalWrite(trigpin, LOW);  //Finishes the trigger pin
  pingtime = pulseIn(echopin, HIGH); // Measures the ping travel time in microseconds 
//  speedofsound =  (2 * distance)/pingtime;  //Calculates in metres per microsecond
//  speedofsound = speedofsound * 1000000;
  speedofsound = 330;               // Speed in metres per microsecond
  distance = speedofsound * pingtime ;
  distance = distance / 1000000 ;
  Serial.print("The speed of sound is ");
//  Serial.print("");
  Serial.print(speedofsound);
  Serial.print("metres per second"); 
  Serial.print("The distance is ");
  Serial.print(distance);
  Serial.println(" metres per second ");
  Serial.print("The pingtime is ");
  Serial.println(pingtime);
  delay(3000);
}
