#include "esp8266_pwm.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"

#ifdef ARDUINO_ESP8266_RELEASE_2_3_0
#error ESP8266 PWM requires at least arduino_core_version 2.4.0
#endif

#include <core_esp8266_waveform.h>

namespace esphome {
namespace esp8266_pwm {

static const char *TAG = "esp8266_pwm";

void ESP8266PWM::setup() {
  ESP_LOGCONFIG(TAG, "Setting up ESP8266 PWM Output...");
  this->pin_->setup();
  this->turn_off();
}
void ESP8266PWM::dump_config() {
  ESP_LOGCONFIG(TAG, "ESP8266 PWM:");
  LOG_PIN("  Pin: ", this->pin_);
  ESP_LOGCONFIG(TAG, "  Frequency: %.1f Hz", this->frequency_);
  LOG_FLOAT_OUTPUT(this);
}
void HOT ESP8266PWM::write_state(float state) {
  this->last_output_ = state;

  // Also check pin inversion
  if (this->pin_->is_inverted()) {
    state = 1.0f - state;
  }

  auto total_time_us = static_cast<uint32_t>(roundf(1e6f / this->frequency_));
  auto duty_on = static_cast<uint32_t>(roundf(total_time_us * state));
  uint32_t duty_off = total_time_us - duty_on;

  if (duty_on == 0) {
    stopWaveform(this->pin_->get_pin());
    this->pin_->digital_write(this->pin_->is_inverted());
  } else if (duty_off == 0) {
    stopWaveform(this->pin_->get_pin());
    this->pin_->digital_write(!this->pin_->is_inverted());
  } else {
    startWaveform(this->pin_->get_pin(), duty_on, duty_off, 0);
  }
}

}  // namespace esp8266_pwm
}  // namespace esphome
