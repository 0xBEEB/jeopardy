#include <avr/io.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdint.h>
#include <util/delay.h>
#include "usb_serial.h"

#define LED_CONFIG	(DDRD |= (1<<6))
#define LED_ON		(PORTD &= ~(1<<6))
#define LED_OFF		(PORTD |= (1<<6))
#define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))

volatile uint8_t unchecked_interrupt;
volatile uint8_t interrupt_pin;

ISR(INT0_vect)
{
	// Handle interrupt
	if(!unchecked_interrupt)
	{
		unchecked_interrupt = 1;
		interrupt_pin = 1;
	}	
}

ISR(INT1_vect)
{
	// Handle interrupt
	if(!unchecked_interrupt)
	{
		unchecked_interrupt = 1;
		interrupt_pin = 2;
	}
}

ISR(INT2_vect)
{
	// Handle interrupt
	if(!unchecked_interrupt)
	{
		unchecked_interrupt = 1;
		interrupt_pin = 3;
	}
}

ISR(INT3_vect)
{
	// Handle interrupt
	if(!unchecked_interrupt)
	{
		unchecked_interrupt = 1;
		interrupt_pin = 4;
	}
}

void setup_gpio(void)
{
	// Set Interrupt 0-3 to trigger on edge to low level
	EICRA = (1<<ISC01) | (1<<ISC11) | (1<<ISC21) | (1<<ISC31);

	PORTD = (1<<PORTD0) | (1<<PORTD1) | (1<<PORTD2) | (1<<PORTD3);
	DDRD = 0;

	


	// Enable interrupt on pins 0-3
	EIMSK = (1<<INT0) | (1<<INT1) | (1<<INT2) | (1<<INT3);
}


// Send a string to the USB serial port.  The string must be in
// flash memory, using PSTR
//
void send_str(const char *s)
{
	char c;
	while (1) {
		c = pgm_read_byte(s++);
		if (!c) break;
		usb_serial_putchar(c);
	}
}

int main(void)
{
	// set for 16 MHz clock, and turn on the LED
	CPU_PRESCALE(0);
	LED_CONFIG;
	LED_ON;

	setup_gpio();
	unchecked_interrupt = 0;

	// initialize the USB, and then wait for the host
	// to set configuration.  If the Teensy is powered
	// without a PC connected to the USB port, this 
	// will wait forever.
	usb_init();
	while (!usb_configured()) /* wait */ ;
	_delay_ms(1000);

	// Turn off LED once we are connected
	LED_OFF;

	// Wait for ready to recieve
	while (!(usb_serial_get_control() & USB_SERIAL_DTR)) /* wait */ ;

	// discard anything that was received prior.  Sometimes the
	// operating system or other software will send a modem
	// "AT command", which can still be buffered.
	usb_serial_flush_input();

	send_str(PSTR("\r\nWelcome to Jeopardy!\r\n"));

	while(1)
	{
		while(!unchecked_interrupt);
		usb_serial_putchar(interrupt_pin);
		unchecked_interrupt = 0;	
	}
}

