import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins, automation
from esphome.const import CONF_ID, CONF_CLK_PIN, CONF_DIO_PIN, CONF_LEVEL, CONF_BRIGHTNESS

tm1651_ns = cg.esphome_ns.namespace('tm1651')
TM1651Display = tm1651_ns.class_('TM1651Display', cg.Component)
SetLevelAction = tm1651_ns.class_('SetLevelAction', automation.Action)
SetBrightnessAction = tm1651_ns.class_('SetBrightnessAction', automation.Action)
validate_level = cv.All(cv.int_range(min=0, max=100))

TM1651_BRIGHTNESS_OPTIONS = {
    1: TM1651Display.TM1651_BRIGHTNESS_LOW,
    2: TM1651Display.TM1651_BRIGHTNESS_MEDIUM,
    3: TM1651Display.TM1651_BRIGHTNESS_HIGH
}

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(TM1651Display),
    cv.Required(CONF_CLK_PIN): pins.internal_gpio_output_pin_schema,
    cv.Required(CONF_DIO_PIN): pins.internal_gpio_output_pin_schema,
})


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)

    clk_pin = yield cg.gpio_pin_expression(config[CONF_CLK_PIN])
    cg.add(var.set_clk_pin(clk_pin))
    dio_pin = yield cg.gpio_pin_expression(config[CONF_DIO_PIN])
    cg.add(var.set_dio_pin(dio_pin))

    # https://platformio.org/lib/show/6865/TM1651
    cg.add_library('6865', '1.0.0')


@automation.register_action('tm1651.set_level', SetLevelAction, cv.maybe_simple_value({
    cv.GenerateID(): cv.use_id(TM1651Display),
    cv.Required(CONF_LEVEL): cv.templatable(validate_level),
}, key=CONF_LEVEL))
def tm1651_set_level_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    yield cg.register_parented(var, config[CONF_ID])
    template_ = yield cg.templatable(config[CONF_LEVEL], args, cg.uint8)
    cg.add(var.set_level(template_))
    yield var


@automation.register_action('tm1651.set_brightness', SetBrightnessAction, cv.maybe_simple_value({
    cv.GenerateID(): cv.use_id(TM1651Display),
    cv.Required(CONF_BRIGHTNESS): cv.templatable(validate_level),
}, key=CONF_BRIGHTNESS))
def tm1651_set_brightness_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    yield cg.register_parented(var, config[CONF_ID])
    template_ = yield cg.templatable(config[CONF_BRIGHTNESS], args, cg.uint8)
    cg.add(var.set_brightness(template_))
    yield var
