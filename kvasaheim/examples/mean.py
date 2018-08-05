class Problem:
    title = 'Mean'
    text = '''The mean is what we usually term the &ldquo;average,&rdquo; although there are many different averages, including the median. The mean is also known as the center of gravity of the data. It is used to estimate the center of a population when the population is not highly skewed. To illustrate calculating the mean, assume that you collected the following values.

    Calculate the mean value of this sample, <span class='statTerm' title="sample mean">\\( \\bar{x} \\)</span>.'''
    category = 'Measures of Center (First Moments)'
    published = True
    equation = '''def solve(x):
      return round(sum(x) / len(x), 4)'''
    random_low = 10
    random_high = 100
    num_rands_low = 5
    num_rands_high = 10
    formula = '''<p class="bodytextno">Here is the formula you can use to calculate the sample mean.</p>
      <div style="margin:0 0 2em 2em;">
      <p>$$ \\bar{x} = \\frac{1}{n} \\sum_{i=1}^{n} x_i $$</p>
      </div>

      <p class="bodytextno">In this formula, there are several symbols to know:</p>
      <div style="margin:0 0 2em 2em;">
        <p class="firstColumn">$$ \\bar{x} $$</p>
            <p class="secondColumn">the sample mean</p>
        <p class="firstColumn">$$ n $$</p><p class="secondColumn">the sample size</p>
        <p class="firstColumn">$$ x_i $$</p><p class="secondColumn">the i<sup>th</sup> data value</p>
        <p class="firstColumn">$$ \\sum $$</p><p class="secondColumn">the act of summing the expression to its right</p>'''
    solution = '''<p>$$ \\begin{align}
        \\bar{x} &= \\frac{1}{n} \\sum_{i=1}^{n} x_i \\\\
        &= \\frac{1}{@length} \\sum_{i=1}^{@length} x_i \\\\
        &= \\frac{1}{@length} \\left( @addition \\right) \\\\
        &= \\frac{1}{ @length } \\left( @sum  \\right) \\\\[1ex]
        &= @answer \\\\
        \\end{align} $$</p>

    <p class="bodytextno">Thus, the mean of these @length values is <span class="highlight">@answer</span>.</p>'''
    rcode = '''<div class="r code">
        <p>sample = c(@list)</p>
        <p>mean(sample)</p>
    </div>
    <p class="bodytextno">In the R output, the mean is the number output by the script.</p>'''
    excel = '''<div class="excel code">
        <p>sample<br />@breaks</p>
        <p>=AVERAGE(A2:A@length1)</p>
    </div>
    <p class="bodytextno">Note that the function in Excel is <code>AVERAGE</code> and <em>not</em> <code>MEAN</code>.</p>'''