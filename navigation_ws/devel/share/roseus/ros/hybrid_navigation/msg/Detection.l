;; Auto-generated. Do not edit!


(when (boundp 'hybrid_navigation::Detection)
  (if (not (find-package "HYBRID_NAVIGATION"))
    (make-package "HYBRID_NAVIGATION"))
  (shadow 'Detection (find-package "HYBRID_NAVIGATION")))
(unless (find-package "HYBRID_NAVIGATION::DETECTION")
  (make-package "HYBRID_NAVIGATION::DETECTION"))

(in-package "ROS")
;;//! \htmlinclude Detection.msg.html


(defclass hybrid_navigation::Detection
  :super ros::object
  :slots (_class_id _class_name _confidence _bbox_center_x _bbox_center_y _distance _angle ))

(defmethod hybrid_navigation::Detection
  (:init
   (&key
    ((:class_id __class_id) 0)
    ((:class_name __class_name) "")
    ((:confidence __confidence) 0.0)
    ((:bbox_center_x __bbox_center_x) 0.0)
    ((:bbox_center_y __bbox_center_y) 0.0)
    ((:distance __distance) 0.0)
    ((:angle __angle) 0.0)
    )
   (send-super :init)
   (setq _class_id (round __class_id))
   (setq _class_name (string __class_name))
   (setq _confidence (float __confidence))
   (setq _bbox_center_x (float __bbox_center_x))
   (setq _bbox_center_y (float __bbox_center_y))
   (setq _distance (float __distance))
   (setq _angle (float __angle))
   self)
  (:class_id
   (&optional __class_id)
   (if __class_id (setq _class_id __class_id)) _class_id)
  (:class_name
   (&optional __class_name)
   (if __class_name (setq _class_name __class_name)) _class_name)
  (:confidence
   (&optional __confidence)
   (if __confidence (setq _confidence __confidence)) _confidence)
  (:bbox_center_x
   (&optional __bbox_center_x)
   (if __bbox_center_x (setq _bbox_center_x __bbox_center_x)) _bbox_center_x)
  (:bbox_center_y
   (&optional __bbox_center_y)
   (if __bbox_center_y (setq _bbox_center_y __bbox_center_y)) _bbox_center_y)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:serialization-length
   ()
   (+
    ;; int32 _class_id
    4
    ;; string _class_name
    4 (length _class_name)
    ;; float32 _confidence
    4
    ;; float32 _bbox_center_x
    4
    ;; float32 _bbox_center_y
    4
    ;; float32 _distance
    4
    ;; float32 _angle
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _class_id
       (write-long _class_id s)
     ;; string _class_name
       (write-long (length _class_name) s) (princ _class_name s)
     ;; float32 _confidence
       (sys::poke _confidence (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _bbox_center_x
       (sys::poke _bbox_center_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _bbox_center_y
       (sys::poke _bbox_center_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _class_id
     (setq _class_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _class_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _class_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _confidence
     (setq _confidence (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _bbox_center_x
     (setq _bbox_center_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _bbox_center_y
     (setq _bbox_center_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _distance
     (setq _distance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _angle
     (setq _angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hybrid_navigation::Detection :md5sum-) "7efc4f850157fd2f62ebe2843f081934")
(setf (get hybrid_navigation::Detection :datatype-) "hybrid_navigation/Detection")
(setf (get hybrid_navigation::Detection :definition-)
      "int32 class_id
string class_name
float32 confidence
float32 bbox_center_x  # Nuevo campo
float32 bbox_center_y  # Nuevo campo
float32 distance       # Opcional para integración con profundidad
float32 angle         # Opcional para posición angular
")



(provide :hybrid_navigation/Detection "7efc4f850157fd2f62ebe2843f081934")


