const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat } = require('docx');
const blocks = JSON.parse(fs.readFileSync('blocks.json', 'utf8'));
const F = 'Calibri';
const kids = [new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: 'Εργασία 2 (MongoDB)', bold: true, size: 32, font: F })] })];
let prevNum = false;
for (const [k, t] of blocks) {
  if (k === 'h') kids.push(new Paragraph({ spacing: { before: 200, after: 120 }, children: [new TextRun({ text: t, bold: true, size: 24, font: F })] }));
  else if (k === 'bullet') kids.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: t, size: 22, font: F })] }));
  else if (k === 'num') kids.push(new Paragraph({ numbering: { reference: 'num', level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: t, size: 22, font: F })] }));
  else { kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: (kids.length && prevNum) ? 200 : 0, after: 160 }, children: [new TextRun({ text: t, size: 22, font: F })] })); }
  prevNum = (k === 'num');
}
const doc = new Document({
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }] }] },
  sections: [{ properties: {}, children: kids }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync('Ergasia2_MongoDB.docx', b); console.log('docx written'); });
