int trigpin = 13;
int echopin = 11;
float pingtime;   // Time required to hit the target and echo back
float speedofsound;
float distance = 0.13;

void setup() 
{  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(trigpin, OUTPUT);  //Sets the trigger as output
  pinMode(echopin, INPUT);   //Sets the trigger as input
  
}

void loop() 
{ // put your main code here, to run repeatedly:
  digitalWrite(trigpin, LOW);
  delayMicroseconds(2000);  // Just give chance for signal to settle down
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);  // Just give chance for signal to settle down
  digitalWrite(trigpin, LOW);  //Finishes the trigger pin
  pingtime = pulseIn(echopin, HIGH); // Measures the ping travel time in microseconds 
  speedofsound =  (2 * distance)/pingtime;  //Calculates in metres per microsecond
  speedofsound = speedofsound * 1000000;
  Serial.print("The speed of sound is ");
  Serial.print(speedofsound);
  Serial.print("  metres per second");
  Serial.println("");
  delay(3000);
}
