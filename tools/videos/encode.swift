// Codifica una carpeta de PNG (f0000.png, f0001.png…) en un MP4 H.264.
// Uso: swift encode.swift <carpeta_frames> <salida.mp4> <fps> <bitrate>
import AVFoundation
import AppKit

let args = CommandLine.arguments
let dir = URL(fileURLWithPath: args[1])
let out = URL(fileURLWithPath: args[2])
let fps = Int32(args[3])!
let bitrate = Int(args[4])!

let files = try FileManager.default.contentsOfDirectory(atPath: dir.path)
  .filter { $0.hasSuffix(".png") }.sorted()
guard let first = NSImage(contentsOf: dir.appendingPathComponent(files[0])),
      let cg0 = first.cgImage(forProposedRect: nil, context: nil, hints: nil) else { fatalError("no frames") }
let w = cg0.width, h = cg0.height

try? FileManager.default.removeItem(at: out)
let writer = try AVAssetWriter(outputURL: out, fileType: .mp4)
let settings: [String: Any] = [
  AVVideoCodecKey: AVVideoCodecType.h264,
  AVVideoWidthKey: w, AVVideoHeightKey: h,
  AVVideoCompressionPropertiesKey: [
    AVVideoAverageBitRateKey: bitrate,
    AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
    AVVideoMaxKeyFrameIntervalKey: Int(fps) * 2,
  ],
]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [
  kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
  kCVPixelBufferWidthKey as String: w, kCVPixelBufferHeightKey as String: h,
])
writer.add(input)
writer.shouldOptimizeForNetworkUse = true
writer.startWriting()
writer.startSession(atSourceTime: .zero)

for (i, name) in files.enumerated() {
  autoreleasepool {
    guard let img = NSImage(contentsOf: dir.appendingPathComponent(name)),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return }
    while !input.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.005) }
    var pb: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &pb)
    guard let buf = pb else { return }
    CVPixelBufferLockBaseAddress(buf, [])
    let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buf), width: w, height: h, bitsPerComponent: 8,
                        bytesPerRow: CVPixelBufferGetBytesPerRow(buf), space: CGColorSpaceCreateDeviceRGB(),
                        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
    CVPixelBufferUnlockBaseAddress(buf, [])
    adaptor.append(buf, withPresentationTime: CMTime(value: CMTimeValue(i), timescale: fps))
  }
}
input.markAsFinished()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
print(writer.status == .completed ? "OK \(out.lastPathComponent) \(files.count) frames \(w)x\(h)" : "ERROR \(String(describing: writer.error))")
