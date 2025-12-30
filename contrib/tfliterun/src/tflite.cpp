#include "tensorflow/contrib/lite/model.h"
#include "tensorflow/contrib/lite/kernels/register.h"

#include <memory>

#include <cassert>

int main(int argc, char **argv)
{
  std::unique_ptr<tflite::FlatBufferModel> model;
  model = tflite::FlatBufferModel::BuildFromFile(argv[1]);

  assert(model != nullptr);

  tflite::ops::builtin::BuiltinOpResolver resolver;

  std::unique_ptr<tflite::Interpreter> interpreter;

  tflite::InterpreterBuilder(*model, resolver)(&interpreter);

  assert(interpreter != nullptr);

  TfLiteStatus status = kTfLiteError;

  status = interpreter->AllocateTensors();
  assert(status == kTfLiteOk);

  status = interpreter->Invoke();
  assert(status == kTfLiteOk);

  return 0;
}
