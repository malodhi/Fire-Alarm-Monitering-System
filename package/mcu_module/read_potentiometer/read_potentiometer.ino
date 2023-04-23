
int potentiometerVal;

void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  sendData();
}

void sendData(){
  potentiometerVal = analogRead(A0);
  //Serial.print("Potentiometer Value => ");
  Serial.println(potentiometerVal);
  //delay(1000);
  }





  
