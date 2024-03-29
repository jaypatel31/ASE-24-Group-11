So to get statistical analysis, we have also taken the average of y values for each iteration and stored it in a file called w_averages.out. This file is used to get the statistical analysis of the data. while w.out represent the normal  output of the code.

# Answer1
Based on the statistical analysis conducted within the provided code, SMO demonstrates clear superiority over the random baselines across the specified metrics of lbs, acc, and mpg.

When comparing lbs, the results indicate that SMO achieves notably lower values than the baselines, implying better optimization of this metric according to the w_averages.out averages. Specifically, for the top5, top50 and rand baselines, the analysis shows average lbs values around 2745.3665, 2897.684, and 2962.4355 respectively over 20 iterations. In contrast, the SMO method yields an average lbs of approximately 2357.4472, markedly outperforming the baselines.

Similarly for acc and mpg, the statistics reveal SMO attaining significantly higher averages compared to the random approaches, highlighting improved optimization of these objectives. While the top5, top50 and rand baselines achieve acc averages around 16.113, 15.7555, and 15.5665, SMO reaches 16.5411, surpassing all three. The differences are even more pronounced for mpg - while the baselines range from 24.2595 to 25.233, SMO accomplishes a 28.9972 average, notably exceeding the alternatives.

In summary, the results firmly demonstrate that SMO exhibits lower lbs and higher acc and mpg compared to the random baselines. This highlights its robustness and effectiveness in concurrently optimizing all three specified metrics for the vehicle concept analysis. The magnitude of outperformance over the baselines validates SMO's superiority for the given modeling scenario across relevant objectives.

# Answer 2

For every Print 3 statements to be printed, we have to find the value which is closest to heaven or minimum d2h value from the entire dataset. And to evaluate that value we need to look at all the y rows present in the data, which are 398 in the auto93.csv file.

# Answer 3

1. **Lbs (Weight)**: The absolute best performance consistently shows a weight of 2130 lbs. Comparatively, the SMO method's average lbs, as shown in the 'mid Average' data, ranges from 2197.84 to 2820.11 lbs. While SMO shows improved performance compared to random baselines, it does not achieve the optimal weight performance of the absolute best.

2. **Acc (Acceleration)**: The absolute best acceleration is consistently 24.6. SMO's acceleration averages are closer, ranging between 15.51 and 16.54. Although SMO performs better than the random baselines, it still falls short of reaching the optimal acceleration performance of the absolute best.

3. **Mpg (Miles Per Gallon)**: The absolute best mpg value is consistently 40. SMO's mpg averages are significantly lower, ranging from 25.23 to 29.42. This indicates that while SMO outperforms the random baselines, it does not reach the level of the absolute best in terms of fuel efficiency.

In summary, the SMO method shows marked improvements over the random baseline methods in optimizing lbs, acc, and mpg. However, when compared to the absolute best performance (print 3), SMO does not achieve the same level of optimization. The absolute best consistently outperforms SMO in all three metrics, indicating there is room for further improvement in SMO's approach to match the optimal results.
