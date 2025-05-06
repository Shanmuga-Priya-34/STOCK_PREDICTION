# STOCK_PREDICTION
A Streamlit-based web application for analyzing stock prices, predicting trends, and calculating profit/loss in INR.



import javax.swing.*;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.dnd.DnDConstants;
import java.awt.dnd.DropTarget;
import java.awt.dnd.DropTargetAdapter;
import java.awt.dnd.DropTargetDropEvent;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.\*;
import javax.imageio.ImageIO;
import javax.imageio.ImageWriter;
import javax.imageio.stream.ImageOutputStream;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;

public class SteganographyGUI extends JFrame {

```
private JLabel imageLabel;

private JTextArea dataTextArea;

private JButton encodeButton;

private JButton decodeButton;

private JButton browseImageButton;

private JProgressBar progressBar;

private JLabel statusLabel;

private BufferedImage droppedImage = null;



public SteganographyGUI() {

    setTitle("Image Steganography");

    setSize(700, 600);

    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    setLayout(new BorderLayout(10, 10));

    JPanel mainPanel = new JPanel();

    mainPanel.setLayout(new GridLayout(6, 1, 5, 5));

    mainPanel.setBorder(new EmptyBorder(10, 10, 10, 10));



    JPanel imagePanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

    imageLabel = new JLabel("Drag and Drop Image Here or Browse");

    imageLabel.setPreferredSize(new Dimension(300, 200));

    imageLabel.setBorder(BorderFactory.createLineBorder(Color.BLACK));

    imageLabel.setHorizontalAlignment(SwingConstants.CENTER);

    imageLabel.setVerticalAlignment(SwingConstants.CENTER);

    makeImageLabelDropTarget();

    imagePanel.add(imageLabel);

    mainPanel.add(imagePanel);



    JPanel browsePanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

    browseImageButton = new JButton("Browse Image");

    browseImageButton.addActionListener(e -> browseImage());

    browsePanel.add(browseImageButton);

    mainPanel.add(browsePanel);



    JPanel dataPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

    dataPanel.add(new JLabel("Data to Encode/Decode:"));

    dataTextArea = new JTextArea(5, 30);

    JScrollPane scrollPane = new JScrollPane(dataTextArea);

    dataPanel.add(scrollPane);

    mainPanel.add(dataPanel);



    JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

    encodeButton = new JButton("Encode");

    decodeButton = new JButton("Decode");

    encodeButton.addActionListener(e -> encodeData());

    decodeButton.addActionListener(e -> decodeData());

    buttonPanel.add(encodeButton);

    buttonPanel.add(decodeButton);

    mainPanel.add(buttonPanel);



    progressBar = new JProgressBar(0, 100);

    mainPanel.add(progressBar);



    statusLabel = new JLabel("");

    statusLabel.setHorizontalAlignment(SwingConstants.CENTER);

    add(mainPanel, BorderLayout.CENTER);

    add(statusLabel, BorderLayout.SOUTH);



    setVisible(true);

}



private void makeImageLabelDropTarget() {

    imageLabel.setDropTarget(new DropTarget(imageLabel, DnDConstants.ACTION_COPY_OR_MOVE, new DropTargetAdapter() {

        @Override

        public void drop(DropTargetDropEvent dtde) {

            try {

                Transferable tr = dtde.getTransferable();

                if (tr.isDataFlavorSupported(DataFlavor.javaFileListFlavor)) {

                    dtde.acceptDrop(DnDConstants.ACTION_COPY_OR_MOVE);

                    List<File> files = (List<File>) tr.getTransferData(DataFlavor.javaFileListFlavor);

                    if (files != null && files.size() == 1) {

                        loadImage(files.get(0));

                    }

                    dtde.dropComplete(true);

                } else if (tr.isDataFlavorSupported(DataFlavor.imageFlavor)) {

                    dtde.acceptDrop(DnDConstants.ACTION_COPY_OR_MOVE);

                    droppedImage = (BufferedImage) tr.getTransferData(DataFlavor.imageFlavor);

                    displayDroppedImage();

                    dtde.dropComplete(true);

                } else {

                    dtde.rejectDrop();

                }

            } catch (Exception ex) {

                ex.printStackTrace();

            }

        }

    }));

}



private void browseImage() {

    JFileChooser fileChooser = new JFileChooser();

    FileNameExtensionFilter filter = new FileNameExtensionFilter("Image Files", "jpg", "jpeg", "png", "gif");

    fileChooser.setFileFilter(filter);

    int returnVal = fileChooser.showOpenDialog(this);

    if (returnVal == JFileChooser.APPROVE_OPTION) {

        File selectedFile = fileChooser.getSelectedFile();

        loadImage(selectedFile);

    }

}



private void loadImage(File imageFile) {

    try {

        droppedImage = ImageIO.read(imageFile);

        if (droppedImage != null) {

            displayDroppedImage();

        } else {

            imageLabel.setText("Invalid Image File");

            imageLabel.setIcon(null);

            droppedImage = null;

        }

    } catch (IOException e) {

        statusLabel.setText("Error loading image: " + e.getMessage());

        imageLabel.setText("Error loading image");

        imageLabel.setIcon(null);

        droppedImage = null;

        e.printStackTrace();

    }

}



private void displayDroppedImage() {

    if (droppedImage != null) {

        ImageIcon imageIcon = new ImageIcon(droppedImage.getScaledInstance(imageLabel.getWidth(), imageLabel.getHeight(), Image.SCALE_SMOOTH));

        imageLabel.setIcon(imageIcon);

        imageLabel.setText("");

    } else {

        imageLabel.setText("No Image Selected");

        imageLabel.setIcon(null);

    }

}



private void encodeData() {

    if (droppedImage == null) {

        statusLabel.setText("Error: No image selected.");

        return;

    }



    String dataToEncode = dataTextArea.getText();

    if (dataToEncode.isEmpty()) {

        statusLabel.setText("Error: No data to encode.");

        return;

    }



    try {

        byte[] data = dataToEncode.getBytes();

        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

        int numThreads = Runtime.getRuntime().availableProcessors();

        int rowsPerThread = droppedImage.getHeight() / numThreads;

        Future<BufferedImage>[] futures = new Future[numThreads];



        for (int i = 0; i < numThreads; i++) {

            int startRow = i * rowsPerThread;

            int endRow = (i == numThreads - 1) ? droppedImage.getHeight() : (i + 1) * rowsPerThread;

            futures[i] = executor.submit(new ImageEncoderTask(droppedImage, data, startRow, endRow));

        }



        BufferedImage encodedImage = new BufferedImage(droppedImage.getWidth(), droppedImage.getHeight(), BufferedImage.TYPE_INT_RGB);

        Graphics g = encodedImage.getGraphics();

        for (int i = 0; i < numThreads; i++) {

            BufferedImage result = futures[i].get();

            g.drawImage(result, 0, i * rowsPerThread, null);

            progressBar.setValue((i + 1) * 100 / numThreads);

        }

        g.dispose();



        JFileChooser fileChooser = new JFileChooser();

        fileChooser.setDialogTitle("Save Encoded Image");

        int userSelection = fileChooser.showSaveDialog(this);

        if (userSelection == JFileChooser.APPROVE_OPTION) {

            File fileToSave = fileChooser.getSelectedFile();

            String fileName = fileToSave.getName();

            String fileExtension = "";

            int dotIndex = fileName.lastIndexOf('.');

            if (dotIndex > 0 && dotIndex < fileName.length() - 1) {

                fileExtension = fileName.substring(dotIndex + 1).toLowerCase();

            }



            String formatName = "png"; // Default to png if original format is unknown or unsupported

            if (fileExtension.equals("jpg") || fileExtension.equals("jpeg")) {

                formatName = "jpeg";

                if (!fileName.toLowerCase().endsWith(".jpg") && !fileName.toLowerCase().endsWith(".jpeg")) {

                    fileToSave = new File(fileToSave.getAbsolutePath() + ".jpg");

                }

            } else if (fileExtension.equals("png")) {

                formatName = "png";

                if (!fileName.toLowerCase().endsWith(".png")) {

                    fileToSave = new File(fileToSave.getAbsolutePath() + ".png");

                }

            } else if (fileExtension.equals("gif")) {

                formatName = "gif";

                if (!fileName.toLowerCase().endsWith(".gif")) {

                    fileToSave = new File(fileToSave.getAbsolutePath() + ".gif");

                }

            } else {

                if (!fileName.toLowerCase().endsWith(".png")) {

                    fileToSave = new File(fileToSave.getAbsolutePath() + ".png");

                }

            }



            try (ImageOutputStream ios = ImageIO.createImageOutputStream(fileToSave)) {

                Iterator<ImageWriter> writers = ImageIO.getImageWritersByFormatName(formatName);

                if (writers.hasNext()) {

                    ImageWriter writer = writers.next();

                    writer.setOutput(ios);

                    writer.write(encodedImage);

                    statusLabel.setText("Encoding Complete. Encoded image saved to " + fileToSave.getAbsolutePath());

                } else {

                    ImageIO.write(encodedImage, "png", fileToSave); // Fallback to PNG

                    statusLabel.setText("Encoding Complete. Encoded image saved to " + fileToSave.getAbsolutePath() + " (saved as PNG due to format issue).");

                }

            } catch (IOException ex) {

                statusLabel.setText("Error saving encoded image: " + ex.getMessage());

                ex.printStackTrace();

            }



        } else {

            statusLabel.setText("Encoding Complete. Save cancelled.");

        }

        executor.shutdown();



    } catch (InterruptedException | ExecutionException ex) {

        statusLabel.setText("Error: " + ex.getMessage());

        ex.printStackTrace();

    }

}



private void decodeData() {

    if (droppedImage == null) {

        statusLabel.setText("Error: No image selected for decoding.");

        return;

    }



    try {

        byte[] decodedDataBytes = DataDecoder.decode(droppedImage);

        String decodedMessage = new String(decodedDataBytes).trim();

        dataTextArea.setText(decodedMessage);

        statusLabel.setText("Decoding Complete.");

        System.out.println("Decoded Message: " + decodedMessage); // For debugging

    } catch (Exception ex) {

        statusLabel.setText("Error decoding data: " + ex.getMessage());

        ex.printStackTrace();

    }

}



public static void main(String[] args) {

    SwingUtilities.invokeLater(SteganographyGUI::new);

}
```

}

class ImageEncoderTask implements Callable<BufferedImage> {
private BufferedImage image;
private byte\[] data;
private int startRow;
private int endRow;

```
public ImageEncoderTask(BufferedImage image, byte[] data, int startRow, int endRow) {

    this.image = image;

    this.data = data;

    this.startRow = startRow;

    this.endRow = endRow;

}



@Override

public BufferedImage call() {

    return DataEncoder.encodePortion(image, data, startRow, endRow);

}
```

}

class DataEncoder {
public static BufferedImage encodePortion(BufferedImage image, byte\[] data, int startRow, int endRow) {
int dataLength = data.length;
int bitIndex = 0;

```
    // Encode data length (first 4 bytes - 32 bits)

    for (int i = 0; i < 32 && bitIndex < image.getWidth() * (endRow - startRow); i++) {

        int y = (startRow * image.getWidth() + bitIndex) / image.getWidth();

        int x = (startRow * image.getWidth() + bitIndex) % image.getWidth();



        int pixel = image.getRGB(x, y);

        int red = (pixel >> 16) & 0xff;

        int green = (pixel >> 8) & 0xff;

        int blue = pixel & 0xff;



        // Get the i-th bit of dataLength

        int lengthBit = (dataLength >> (31 - i)) & 1;

        // Set the LSB of blue to the length bit

        blue = (blue & 0xFE) | lengthBit;



        pixel = (red << 16) | (green << 8) | blue;

        image.setRGB(x, y, pixel);

        bitIndex++;

    }



    // Encode the actual data

    int dataByteIndex = 0;

    int dataBitIndex = 0;

    while (dataByteIndex < dataLength && bitIndex < image.getWidth() * (endRow - startRow)) {

        int y = (startRow * image.getWidth() + bitIndex) / image.getWidth();

        int x = (startRow * image.getWidth() + bitIndex) % image.getWidth();



        int pixel = image.getRGB(x, y);

        int red = (pixel >> 16) & 0xff;

        int green = (pixel >> 8) & 0xff;

        int blue = pixel & 0xff;



        // Get the current bit from the data byte

        int dataBit = (data[dataByteIndex] >> (7 - dataBitIndex)) & 1;

        // Set the LSB of blue to the data bit

        blue = (blue & 0xFE) | dataBit;



        pixel = (red << 16) | (green << 8) | blue;

        image.setRGB(x, y, pixel);



        dataBitIndex++;

        if (dataBitIndex == 8) {

            dataBitIndex = 0;

            dataByteIndex++;

        }

        bitIndex++;

    }

    return image;

}
```

}

class DataDecoder {
public static byte\[] decode(BufferedImage image) {
int imageWidth = image.getWidth();
int imageHeight = image.getHeight();
int maxDataLengthBytes = (imageWidth \* imageHeight) / 8;
ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
int bitIndex = 0;

```
    int encodedDataLength = 0;

    // Read the data length (first 4 bytes - 32 bits)

    for (int i = 0; i < 32 && bitIndex < imageWidth * imageHeight; i++) {

        int y = bitIndex / imageWidth;

        int x = bitIndex % imageWidth;



        int pixel = image.getRGB(x, y);

        int blue = pixel & 0xff;

        int bit = (blue & 1);

        encodedDataLength |= (bit << (31 - i));

        bitIndex++;

    }



    if (encodedDataLength > maxDataLengthBytes) {

        System.err.println("Warning: Embedded data length exceeds maximum possible.");

        return new byte[0];

    }



    int decodedBytes = 0;

    int currentByte = 0;

    int bitInByte = 0;



    // Read the actual data

    while (decodedBytes < encodedDataLength && bitIndex < imageWidth * imageHeight) {

        int y = bitIndex / imageWidth;

        int x = bitIndex % imageWidth;



        int pixel = image.getRGB(x, y);

        int blue = pixel & 0xff;

        int bit = (blue & 1);



        currentByte |= (bit << (7 - bitInByte));



        bitInByte++;

        if (bitInByte == 8) {

            outputStream.write(currentByte);

            currentByte = 0;

            bitInByte = 0;

            decodedBytes++;

        }

        bitIndex++;

    }



    return outputStream.toByteArray();

}
```

}




