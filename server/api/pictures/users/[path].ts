import { defineEventHandler } from 'h3';
import fs from 'fs';
import path from 'path';

export default defineEventHandler(async (event) => {
    const url = event.node.req.url; // Получаем запрошенный путь
    const fileName = url!.replace('/api/pictures/users/', '');
    const filePath = path.join(process.cwd(), 'pictures/users', fileName);
    const error = path.join(process.cwd(), 'pictures/users', '/default.png');

    if (!fs.existsSync(filePath)) {
        const fileStream = fs.createReadStream(error);
        return sendStream(event, fileStream);

    } else {
        const fileStream = fs.createReadStream(filePath);
        return sendStream(event, fileStream);
    }

});