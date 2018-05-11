#define CONTROL_BIT 1
#define ACTIVATION_BIT 0

/*
 * Returns the physical port number for the desired item.
 * Parameters: 
 *    index - index of the external port (P0, P1 or P2) to get.
 *    type - Can pass CONTROL_BIT to get the controlling port or ACTIVATION_BIT to get the safety switch port.
 */
int getPort(int index, int type) {
  return 2 + type + 2 * index;
}

/*
 * Defines all relevant ports to OUTPUT pin mode.
 */
void defineOutputs() {
  for (int i = 2; i < 8; i++) {
    pinMode(i, OUTPUT);
  }
}

void activate(int port, bool activate) {
  digitalWrite(getPort(port, ACTIVATION_BIT), 1 - activate);
  delay(40);
}

void flip(int port, bool flip) {
  digitalWrite(getPort(port, CONTROL_BIT), 1 - flip);
  delay(40);
}

void safety() {
  for (int i = 0; i < 3; i++) {
    activate(i, false);
    flip(i, false);
  }
}

void setup() {
  // put your setup code here, to run once:
  defineOutputs();
  safety();
  Serial.begin(9600);
}

/*
 * Reads a command from the serial connection.
 */
String readCmd() {
  String cmd("");
  while (true) {
    while (Serial.available() == 0) ;
    char x = Serial.read();
    if (x == ';') {
      return cmd;
    }
    else {
      cmd = cmd + x;
    }
  }
}

void cmdOn(String cmd) {
  char x = cmd[3];
  Serial.println(x);
  if (x >= '0' && x <= '2') {
    activate(x - '0', true);
  }
}

void cmdOff(String cmd) {
  char x = cmd[3];
  if (x >= '0' && x <= '2') {
    activate(x - '0', false);
  }
}

void cmdStraight(String cmd) {
  char x = cmd[3];
  if (x >= '0' && x <= '2') {
    activate(x - '0', false);
    flip(x - '0', false);
    activate(x - '0', true);
  }
}

void cmdFlip(String cmd) {
  char x = cmd[3];
  if (x >= '0' && x <= '2') {
    activate(x - '0', false);
    flip(x - '0', true);
    activate(x - '0', true);
  }
}

void cmdInfo(String cmd) {
  Serial.println("Software: CurrentFlipper V0.1.3;");
}

void loop() {
  String c = readCmd();
  if (c.startsWith("ONN")) {
    cmdOn(c);
  }
  else if (c.startsWith("OFF")) {
    cmdOff(c);
  }
  else if (c.startsWith("FLP")) {
    cmdFlip(c);
  }
  else if (c.startsWith("STR")) {
    cmdStraight(c);
  }
  else if (c.startsWith("INF")) {
    cmdInfo(c);
  }
}
