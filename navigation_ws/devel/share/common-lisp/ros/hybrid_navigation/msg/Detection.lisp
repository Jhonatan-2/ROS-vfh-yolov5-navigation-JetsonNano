; Auto-generated. Do not edit!


(cl:in-package hybrid_navigation-msg)


;//! \htmlinclude Detection.msg.html

(cl:defclass <Detection> (roslisp-msg-protocol:ros-message)
  ((class_id
    :reader class_id
    :initarg :class_id
    :type cl:integer
    :initform 0)
   (class_name
    :reader class_name
    :initarg :class_name
    :type cl:string
    :initform "")
   (confidence
    :reader confidence
    :initarg :confidence
    :type cl:float
    :initform 0.0)
   (bbox_center_x
    :reader bbox_center_x
    :initarg :bbox_center_x
    :type cl:float
    :initform 0.0)
   (bbox_center_y
    :reader bbox_center_y
    :initarg :bbox_center_y
    :type cl:float
    :initform 0.0)
   (distance
    :reader distance
    :initarg :distance
    :type cl:float
    :initform 0.0)
   (angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0))
)

(cl:defclass Detection (<Detection>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Detection>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Detection)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hybrid_navigation-msg:<Detection> is deprecated: use hybrid_navigation-msg:Detection instead.")))

(cl:ensure-generic-function 'class_id-val :lambda-list '(m))
(cl:defmethod class_id-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:class_id-val is deprecated.  Use hybrid_navigation-msg:class_id instead.")
  (class_id m))

(cl:ensure-generic-function 'class_name-val :lambda-list '(m))
(cl:defmethod class_name-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:class_name-val is deprecated.  Use hybrid_navigation-msg:class_name instead.")
  (class_name m))

(cl:ensure-generic-function 'confidence-val :lambda-list '(m))
(cl:defmethod confidence-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:confidence-val is deprecated.  Use hybrid_navigation-msg:confidence instead.")
  (confidence m))

(cl:ensure-generic-function 'bbox_center_x-val :lambda-list '(m))
(cl:defmethod bbox_center_x-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:bbox_center_x-val is deprecated.  Use hybrid_navigation-msg:bbox_center_x instead.")
  (bbox_center_x m))

(cl:ensure-generic-function 'bbox_center_y-val :lambda-list '(m))
(cl:defmethod bbox_center_y-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:bbox_center_y-val is deprecated.  Use hybrid_navigation-msg:bbox_center_y instead.")
  (bbox_center_y m))

(cl:ensure-generic-function 'distance-val :lambda-list '(m))
(cl:defmethod distance-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:distance-val is deprecated.  Use hybrid_navigation-msg:distance instead.")
  (distance m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <Detection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hybrid_navigation-msg:angle-val is deprecated.  Use hybrid_navigation-msg:angle instead.")
  (angle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Detection>) ostream)
  "Serializes a message object of type '<Detection>"
  (cl:let* ((signed (cl:slot-value msg 'class_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'class_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'class_name))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'confidence))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'bbox_center_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'bbox_center_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'distance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Detection>) istream)
  "Deserializes a message object of type '<Detection>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'class_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'class_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'class_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'confidence) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'bbox_center_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'bbox_center_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'distance) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Detection>)))
  "Returns string type for a message object of type '<Detection>"
  "hybrid_navigation/Detection")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Detection)))
  "Returns string type for a message object of type 'Detection"
  "hybrid_navigation/Detection")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Detection>)))
  "Returns md5sum for a message object of type '<Detection>"
  "7efc4f850157fd2f62ebe2843f081934")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Detection)))
  "Returns md5sum for a message object of type 'Detection"
  "7efc4f850157fd2f62ebe2843f081934")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Detection>)))
  "Returns full string definition for message of type '<Detection>"
  (cl:format cl:nil "int32 class_id~%string class_name~%float32 confidence~%float32 bbox_center_x  # Nuevo campo~%float32 bbox_center_y  # Nuevo campo~%float32 distance       # Opcional para integración con profundidad~%float32 angle         # Opcional para posición angular~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Detection)))
  "Returns full string definition for message of type 'Detection"
  (cl:format cl:nil "int32 class_id~%string class_name~%float32 confidence~%float32 bbox_center_x  # Nuevo campo~%float32 bbox_center_y  # Nuevo campo~%float32 distance       # Opcional para integración con profundidad~%float32 angle         # Opcional para posición angular~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Detection>))
  (cl:+ 0
     4
     4 (cl:length (cl:slot-value msg 'class_name))
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Detection>))
  "Converts a ROS message object to a list"
  (cl:list 'Detection
    (cl:cons ':class_id (class_id msg))
    (cl:cons ':class_name (class_name msg))
    (cl:cons ':confidence (confidence msg))
    (cl:cons ':bbox_center_x (bbox_center_x msg))
    (cl:cons ':bbox_center_y (bbox_center_y msg))
    (cl:cons ':distance (distance msg))
    (cl:cons ':angle (angle msg))
))
