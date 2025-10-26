const fs = require('fs');
const path = require('path');

// Source logo from landing page
const sourceLogo = path.join(__dirname, '..', 'Landing page', 'Aegis.PNG');
const targetDir = path.join(__dirname, 'images');

// Create images directory if it doesn't exist
if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
}

// Copy the logo to different sizes
const sizes = [16, 32, 48, 128];

// Function to copy and resize image
function copyAndResizeImage(source, target, size) {
    try {
        // For now, just copy the file with the new name
        // In a real scenario, you would use an image processing library
        const ext = path.extname(source);
        const targetPath = path.join(target, `icon${size}${ext}`);
        fs.copyFileSync(source, targetPath);
        console.log(`Created: ${targetPath}`);
    } catch (error) {
        console.error(`Error processing ${size}x${size} icon:`, error);
    }
}

// Process each size
sizes.forEach(size => {
    copyAndResizeImage(sourceLogo, targetDir, size);
});

console.log('Icons updated successfully!');
