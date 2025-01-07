package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/DrmagicE/gmqtt"
	"github.com/DrmagicE/gmqtt/pkg/packets"
)

func main() {
	// Create a new MQTT broker
	broker := gmqtt.NewBroker()

	// Define a hook to log messages
	broker.RegisterHook(newLoggingHook())

	// Start the broker in a separate goroutine
	go func() {
		fmt.Println("Starting MQTT broker on :1883")
		if err := broker.Run(); err != nil {
			log.Fatalf("Error starting broker: %v", err)
		}
	}()

	// Graceful shutdown on interrupt or terminate signal
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
	<-sigCh

	fmt.Println("\nShutting down MQTT broker...")
	if err := broker.Close(); err != nil {
		log.Fatalf("Error shutting down broker: %v", err)
	}
	fmt.Println("MQTT broker stopped.")
}

// loggingHook is a simple hook to log MQTT messages
type loggingHook struct{}

func newLoggingHook() *loggingHook {
	return &loggingHook{}
}

// OnConnect logs when a client connects
func (h *loggingHook) OnConnect(client *gmqtt.Client) {
	log.Printf("Client connected: %s", client.ClientID())
}

// OnSubscribe logs when a client subscribes to a topic
func (h *loggingHook) OnSubscribe(client *gmqtt.Client, packets []*gmqtt.Subscription) {
	for _, packet := range packets {
		log.Printf("Client %s subscribed to topic: %s", client.ClientID(), packet.TopicName)
	}
}

// OnPublish logs when a message is published
func (h *loggingHook) OnPublish(client *gmqtt.Client, packet *packets.Publish) {
	log.Printf("Message published to topic %s: %s", packet.TopicName, string(packet.Payload))
}

// OnDisconnect logs when a client disconnects
func (h *loggingHook) OnDisconnect(client *gmqtt.Client, err error) {
	log.Printf("Client disconnected: %s, reason: %v", client.ClientID(), err)
}

// OnClose is called when the broker is closed
func (h *loggingHook) OnClose() {
	log.Println("Broker is shutting down...")
}

