
"use strict";

let Keypoint2Di = require('./Keypoint2Di.js');
let BoundingBox2Di = require('./BoundingBox2Di.js');
let Keypoint3D = require('./Keypoint3D.js');
let Skeleton3D = require('./Skeleton3D.js');
let Object = require('./Object.js');
let ObjectsStamped = require('./ObjectsStamped.js');
let Keypoint2Df = require('./Keypoint2Df.js');
let RGBDSensors = require('./RGBDSensors.js');
let BoundingBox2Df = require('./BoundingBox2Df.js');
let BoundingBox3D = require('./BoundingBox3D.js');
let PosTrackStatus = require('./PosTrackStatus.js');
let PlaneStamped = require('./PlaneStamped.js');
let Skeleton2D = require('./Skeleton2D.js');

module.exports = {
  Keypoint2Di: Keypoint2Di,
  BoundingBox2Di: BoundingBox2Di,
  Keypoint3D: Keypoint3D,
  Skeleton3D: Skeleton3D,
  Object: Object,
  ObjectsStamped: ObjectsStamped,
  Keypoint2Df: Keypoint2Df,
  RGBDSensors: RGBDSensors,
  BoundingBox2Df: BoundingBox2Df,
  BoundingBox3D: BoundingBox3D,
  PosTrackStatus: PosTrackStatus,
  PlaneStamped: PlaneStamped,
  Skeleton2D: Skeleton2D,
};
