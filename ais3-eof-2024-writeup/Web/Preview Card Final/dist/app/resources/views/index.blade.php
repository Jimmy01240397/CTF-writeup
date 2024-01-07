<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview Card</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
</head>

<body>
    <section class="section">
        <div class="container">
            <div class="column is-6 is-offset-3 has-text-centered">
                <h1 class="title">Web Preview Card</h1>
                <a href="/preview?url=https://example.com/">Try it!</a>
                @if (session('url'))
                | <a href="/preview?url={{ session('url') }}">Previous Request</a>
                @endif
            </div>
        </div>
    </section>
</body>

</html>
