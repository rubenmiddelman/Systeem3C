int sensorPin = 15;
int ledPin = 13; 
int sensorVal = 0;  
int startSensorVal = 0;
int secondSensorVal = 0;
int checkerVal = 0;
int counter = 0;
int pinOutput = 0;


void setup() {
  pinMode(ledPin, OUTPUT); 
  Serial.begin(9600);
}

void loop() {
  // makes a state change finder so that i counts how mant times a light disapears from the LDR so that ou kan count the jumping jacks 
  sensorVal = analogRead(sensorPin);    
  digitalWrite(ledPin, LOW);
  startSensorVal = sensorVal;
  delay(50);
  sensorVal = analogRead(sensorPin); 
  secondSensorVal = sensorVal;
  checkerVal = startSensorVal - secondSensorVal;
  if(checkerVal > 100){
    counter++;
    Serial.println(counter);//data that is being Sent
  }

  
  
}
