# Trained AI Policy Models (`models/`)

This directory contains pre-trained neural network policies deployed via ONNX Runtime for edge inference on the Qualcomm QRB2210.

## Files

- `policies/sample_policy.onnx`: Reference ONNX policy taking `(1, 3, 224, 320)` RGB frame inputs and predicting 12 discrete Genesis button logits.
- `metadata/model.json`: Specification of tensor shapes, data types, execution providers, and training hyperparameters.

## Exporting Your Own Policy

To export a PyTorch model to ONNX for UNO Q Arena:

```python
import torch
import torch.onnx

model = MyStreetFighterPolicy()
model.eval()

dummy_input = torch.randn(1, 3, 224, 320, dtype=torch.float32)

torch.onnx.export(
    model,
    dummy_input,
    "models/policies/my_custom_policy.onnx",
    input_names=["screen_frame"],
    output_names=["button_logits"],
    opset_version=17
)
```

## Hardware Acceleration

- **Qualcomm QRB2210 Linux**: Uses `CPUExecutionProvider` or Qualcomm Hexagon NPU via QNN Execution Provider.
- **macOS Dev / Testing**: Automatically leverages Apple Silicon CoreML via `CoreMLExecutionProvider`.
