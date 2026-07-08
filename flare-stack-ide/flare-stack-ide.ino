const int ldrPin = A0;
const int potPin = A1;
const int buttonPin = 2;
const int greenLed = 8;
const int redLed = 9;
const int buzzerPin = 10;

bool alarmMuted = false;
bool ledsEnabled = true;
bool lastButtonState = LOW;
String currentMode = "DAY"; 

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "MUTE") {
      alarmMuted = !alarmMuted; 
    } else if (cmd == "LED") {
      ledsEnabled = !ledsEnabled; 
    } else if (cmd.startsWith("MODE:")) {
      currentMode = cmd.substring(5); 
    }
  }

  int flameLevel = analogRead(ldrPin);
  int potValue = analogRead(potPin);
  
  int activeThreshold = potValue;
  if (currentMode == "NIGHT") {
    activeThreshold = potValue - 80; 
    if (activeThreshold < 0) activeThreshold = 0;
  }
  int currentButtonState = digitalRead(buttonPin);
  if (currentButtonState == HIGH && lastButtonState == LOW) {
    alarmMuted = !alarmMuted;
    delay(50);
  }
  lastButtonState = currentButtonState;

  String status = "NORMAL";
  
  if (flameLevel > activeThreshold) { 
    status = "ALARM";
    if (ledsEnabled) {
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, HIGH);
    } else {
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, LOW);
    }
    
    if (!alarmMuted) tone(buzzerPin, 1000);
    else noTone(buzzerPin);
    
  } else { 
    if (ledsEnabled) {
      digitalWrite(greenLed, HIGH);
      digitalWrite(redLed, LOW);
    } else {
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, LOW);
    }
    noTone(buzzerPin);
  }

  Serial.print(status); Serial.print(":");
  Serial.print(flameLevel); Serial.print(":");
  Serial.print(activeThreshold); Serial.print(":");
  Serial.print(alarmMuted ? "1" : "0"); Serial.print(":");
  Serial.println(ledsEnabled ? "1" : "0");

  delay(200); 
}