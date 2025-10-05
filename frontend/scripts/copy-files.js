import fs from 'fs/promises';
import path from 'path';

async function copyFiles() {
    try {
        const sourceProductFile = path.join(process.cwd(), 'pictures', 'products', 'default-product.jpg');
        const sourceUserFile = path.join(process.cwd(), 'pictures', 'users', 'default.png');

        const outputDir = path.join(process.cwd(), '.output');
        const picturesDir = path.join(outputDir, 'pictures');
        const productsDir = path.join(picturesDir, 'products');
        const usersDir = path.join(picturesDir, 'users');

        await fs.mkdir(productsDir, { recursive: true });
        await fs.mkdir(usersDir, { recursive: true });

        await fs.copyFile(sourceProductFile, path.join(productsDir, 'default-product.jpg'));
        await fs.copyFile(sourceUserFile, path.join(usersDir, 'default.png'));
    } catch (error) {
        console.error('Ошибка при копировании файлов:', error);
    }
}

copyFiles();
