const express = require('express');
const app = express();

const TITLE = process.env.TITLE || 'HTML Debugger'
const PORT = process.env.PORT || 3000

app.set('view engine', 'ejs');

app.use(express.json());

app.use(express.static('static'));

app.post('/preview', (req, res) => res.json({
  html: req.body.html
}));

app.get('*', (req, res) => {
  const { html="" } = req.query;
  res.render("index", { TITLE, html: encodeURIComponent(html)});
});

app.listen(PORT, () => {
  console.log(`Listening on http://localhost:${PORT}`)
})
