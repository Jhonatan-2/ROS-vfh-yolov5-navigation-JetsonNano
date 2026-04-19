// Auto-generated. Do not edit!

// (in-package hybrid_navigation.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Detection {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.class_id = null;
      this.class_name = null;
      this.confidence = null;
      this.bbox_center_x = null;
      this.bbox_center_y = null;
      this.distance = null;
      this.angle = null;
    }
    else {
      if (initObj.hasOwnProperty('class_id')) {
        this.class_id = initObj.class_id
      }
      else {
        this.class_id = 0;
      }
      if (initObj.hasOwnProperty('class_name')) {
        this.class_name = initObj.class_name
      }
      else {
        this.class_name = '';
      }
      if (initObj.hasOwnProperty('confidence')) {
        this.confidence = initObj.confidence
      }
      else {
        this.confidence = 0.0;
      }
      if (initObj.hasOwnProperty('bbox_center_x')) {
        this.bbox_center_x = initObj.bbox_center_x
      }
      else {
        this.bbox_center_x = 0.0;
      }
      if (initObj.hasOwnProperty('bbox_center_y')) {
        this.bbox_center_y = initObj.bbox_center_y
      }
      else {
        this.bbox_center_y = 0.0;
      }
      if (initObj.hasOwnProperty('distance')) {
        this.distance = initObj.distance
      }
      else {
        this.distance = 0.0;
      }
      if (initObj.hasOwnProperty('angle')) {
        this.angle = initObj.angle
      }
      else {
        this.angle = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Detection
    // Serialize message field [class_id]
    bufferOffset = _serializer.int32(obj.class_id, buffer, bufferOffset);
    // Serialize message field [class_name]
    bufferOffset = _serializer.string(obj.class_name, buffer, bufferOffset);
    // Serialize message field [confidence]
    bufferOffset = _serializer.float32(obj.confidence, buffer, bufferOffset);
    // Serialize message field [bbox_center_x]
    bufferOffset = _serializer.float32(obj.bbox_center_x, buffer, bufferOffset);
    // Serialize message field [bbox_center_y]
    bufferOffset = _serializer.float32(obj.bbox_center_y, buffer, bufferOffset);
    // Serialize message field [distance]
    bufferOffset = _serializer.float32(obj.distance, buffer, bufferOffset);
    // Serialize message field [angle]
    bufferOffset = _serializer.float32(obj.angle, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Detection
    let len;
    let data = new Detection(null);
    // Deserialize message field [class_id]
    data.class_id = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [class_name]
    data.class_name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [confidence]
    data.confidence = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [bbox_center_x]
    data.bbox_center_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [bbox_center_y]
    data.bbox_center_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [distance]
    data.distance = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [angle]
    data.angle = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.class_name.length;
    return length + 28;
  }

  static datatype() {
    // Returns string type for a message object
    return 'hybrid_navigation/Detection';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7efc4f850157fd2f62ebe2843f081934';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 class_id
    string class_name
    float32 confidence
    float32 bbox_center_x  # Nuevo campo
    float32 bbox_center_y  # Nuevo campo
    float32 distance       # Opcional para integración con profundidad
    float32 angle         # Opcional para posición angular
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Detection(null);
    if (msg.class_id !== undefined) {
      resolved.class_id = msg.class_id;
    }
    else {
      resolved.class_id = 0
    }

    if (msg.class_name !== undefined) {
      resolved.class_name = msg.class_name;
    }
    else {
      resolved.class_name = ''
    }

    if (msg.confidence !== undefined) {
      resolved.confidence = msg.confidence;
    }
    else {
      resolved.confidence = 0.0
    }

    if (msg.bbox_center_x !== undefined) {
      resolved.bbox_center_x = msg.bbox_center_x;
    }
    else {
      resolved.bbox_center_x = 0.0
    }

    if (msg.bbox_center_y !== undefined) {
      resolved.bbox_center_y = msg.bbox_center_y;
    }
    else {
      resolved.bbox_center_y = 0.0
    }

    if (msg.distance !== undefined) {
      resolved.distance = msg.distance;
    }
    else {
      resolved.distance = 0.0
    }

    if (msg.angle !== undefined) {
      resolved.angle = msg.angle;
    }
    else {
      resolved.angle = 0.0
    }

    return resolved;
    }
};

module.exports = Detection;
