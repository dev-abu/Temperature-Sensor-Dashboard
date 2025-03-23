import serial

try:
    ser = serial.Serial('COM9', 9600)
    print("✅ Serial port COM9 opened successfully!")
    ser.close()
except serial.SerialException as e:
    print("❌ Could not open COM9:", e)
