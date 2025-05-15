# Using Flutter Dio with the Flight Ticket OCR API

Here's how you can use the Dio package in Flutter to interact with the Flight Ticket OCR API:

## 1. Add Dio to your Flutter project

First, add the Dio package to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.3.2
  http_parser: ^4.0.2
```

Then run:

```bash
flutter pub get
```

## 2. Implementation Example

Here's a complete example of how to use Dio to upload a flight ticket image/PDF and process it:

```dart
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http_parser/http_parser.dart';
import 'package:path/path.dart' as path;

class FlightTicketOcrService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://localhost:8808',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 60),
  ));

  /// Extracts information from a flight ticket file
  /// 
  /// [file] - The flight ticket file (image or PDF)
  /// [model] - Optional AI model to use for processing
  Future<Map<String, dynamic>> extractTicketInfo(
    File file, {
    String model = 'deepseek/deepseek-chat-v3-0324:free',
  }) async {
    try {
      // Determine file mime type
      final extension = path.extension(file.path).toLowerCase();
      String mimeType;
      
      if (extension == '.pdf') {
        mimeType = 'application/pdf';
      } else if (extension == '.png') {
        mimeType = 'image/png';
      } else if (extension == '.jpg' || extension == '.jpeg') {
        mimeType = 'image/jpeg';
      } else {
        throw Exception('Unsupported file type: $extension');
      }

      // Create form data
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          file.path,
          filename: path.basename(file.path),
          contentType: MediaType.parse(mimeType),
        ),
        'model': model,
      });

      // Make the API request
      final response = await _dio.post(
        '/api/extract',
        data: formData,
      );

      return response.data;
    } on DioException catch (e) {
      if (e.response != null) {
        // The server responded with an error
        final errorMessage = e.response?.data['error'] ?? 'Failed to extract ticket information';
        throw Exception(errorMessage);
      } else {
        // No response from server or connection error
        throw Exception('Network error: ${e.message}');
      }
    } catch (e) {
      throw Exception('Error: ${e.toString()}');
    }
  }
}

// Example Flutter widget to use the service
class TicketScannerScreen extends StatefulWidget {
  const TicketScannerScreen({Key? key}) : super(key: key);

  @override
  State<TicketScannerScreen> createState() => _TicketScannerScreenState();
}

class _TicketScannerScreenState extends State<TicketScannerScreen> {
  final FlightTicketOcrService _ocrService = FlightTicketOcrService();
  final ImagePicker _picker = ImagePicker();
  
  File? _selectedFile;
  Map<String, dynamic>? _result;
  bool _isLoading = false;
  String? _error;

  Future<void> _pickImage() async {
    final XFile? pickedFile = await _picker.pickImage(source: ImageSource.gallery);
    
    if (pickedFile != null) {
      setState(() {
        _selectedFile = File(pickedFile.path);
        _result = null;
        _error = null;
      });
    }
  }

  Future<void> _pickPdf() async {
    // You would need a file picker package for PDFs
    // This is just a placeholder
    // final FilePickerResult? result = await FilePicker.platform.pickFiles(
    //   type: FileType.custom,
    //   allowedExtensions: ['pdf'],
    // );
    
    // if (result != null) {
    //   setState(() {
    //     _selectedFile = File(result.files.single.path!);
    //     _result = null;
    //     _error = null;
    //   });
    // }
  }

  Future<void> _processTicket() async {
    if (_selectedFile == null) return;
    
    setState(() {
      _isLoading = true;
      _error = null;
    });
    
    try {
      final result = await _ocrService.extractTicketInfo(_selectedFile!);
      setState(() {
        _result = result;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flight Ticket Scanner'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.image),
              label: const Text('Select Image'),
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              onPressed: _pickPdf,
              icon: const Icon(Icons.picture_as_pdf),
              label: const Text('Select PDF'),
            ),
            const SizedBox(height: 16),
            if (_selectedFile != null) ...[
              Text('Selected file: ${path.basename(_selectedFile!.path)}'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _isLoading ? null : _processTicket,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Process Ticket'),
              ),
            ],
            if (_error != null) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(8),
                color: Colors.red.shade100,
                child: Text(
                  _error!,
                  style: TextStyle(color: Colors.red.shade900),
                ),
              ),
            ],
            if (_result != null) ...[
              const SizedBox(height: 16),
              const Text(
                'Extracted Information:',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    for (var entry in _result!.entries)
                      if (entry.value != null) ...[
                        Text(
                          '${entry.key}:',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        Text(entry.value.toString()),
                        const SizedBox(height: 8),
                      ],
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

## 3. Additional Notes

1. **Error Handling**: The example includes comprehensive error handling for network issues and server errors.

2. **File Type Detection**: The code determines the MIME type based on the file extension to properly set the content type for the upload.

3. **Dependencies**: You'll need additional packages:
   - `image_picker` for selecting images
   - `http_parser` for handling MIME types
   - For PDF selection, you might want to add `file_picker`

4. **Local API**: Remember that the API is running locally on port 8808. For a real mobile app, you would need:
   - The API hosted on a publicly accessible server
   - Updated baseUrl in the Dio configuration
   - For Android, add internet permission in the manifest

5. **iOS Configuration**: For iOS, you'll need to add permissions in Info.plist for accessing the photo library.

This implementation provides a complete solution for integrating your Flight Ticket OCR API with a Flutter mobile application using Dio for HTTP requests.