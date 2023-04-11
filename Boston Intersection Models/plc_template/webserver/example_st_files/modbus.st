FUNCTION_BLOCK Generator
  VAR_OUTPUT
    OUT : BOOL;
  END_VAR
  VAR_INPUT
    PON : TIME;
    POFF : TIME;
  END_VAR
  VAR
    T1 : TON;
    T2 : TOF;
  END_VAR

  T1( IN := NOT T2.Q, PT := POFF);
  T2( IN := T1.Q,     PT := PON);
  OUT := T2.Q;
END_FUNCTION_BLOCK

PROGRAM program0
  VAR
    Counter : INT;
    CounterReadBack : INT;
  END_VAR
  VAR
    MasterWriteToReg0 AT %QW0.0.0.0 : INT;
    MasterReadFromReg1 AT %IW0.0.1.0 : INT;
    SlaveHoldReg0 AT %IW0.1.0.0 : WORD;
    SlaveInputReg0 AT %QW0.1.1.0 : WORD;
  END_VAR
  VAR
    CTU0 : CTU;
    Generator0 : Generator;
    R_TRIG1 : R_TRIG;
  END_VAR

  Generator0(PON := T#1s, POFF := T#1s);
  R_TRIG1(CLK := Generator0.OUT);
  CTU0(CU := R_TRIG1.Q, PV := 32767);
  Counter := CTU0.CV;
  MasterWriteToReg0 := Counter;
  CounterReadBack := MasterReadFromReg1;
  SlaveInputReg0 := SlaveHoldReg0;
END_PROGRAM


CONFIGURATION config

  RESOURCE resource1 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
