#define SWITCH_PIN 12
#define PIR_PIN 11
#define LED_PIN 13

void setup() {
  pinMode(SWITCH_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(digitalRead(SWITCH_PIN) == 1){
    digitalWrite(LED_PIN, HIGH); 
  }else{
    digitalWrite(LED_PIN, LOW);
  }
  
  if(digitalRead(PIR_PIN) == 1){
    Serial.println("move");
  }else{
    Serial.println("still");
  }
}
