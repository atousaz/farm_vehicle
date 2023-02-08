avg_dist = smooth_scatter(data, 30)
    segments = slidingwindowsegment(
        avg_dist, poly_regression, poly_sumsquared_error, max_error=10, min_range=30)
    segments = update_segments(avg_dist, segments, min_range=30)
    x = np.arange(len(data))/30
    y = data
    t = [i[0]/30 for i in segments]
#     print(x)
#     print(y)
#     print(t)
    try:
        spl = LSQUnivariateSpline(x, y, t[1:], k=3)
#     print("spl: ", spl)
    except:
        return 0, 0, 0, 0
    if plot:
        fig, ax = plt.subplots(1, 1, figsize=(12, 4))
        draw_segments(avg_dist, segments, ax, spl)
        # draw_vel(avg_dist, segments, ax, spl)
        ax.plot(np.arange(len(data))/30,
                data, 'go', ms=5, alpha=.05)

    vel, acc, classes = clasify_segments(avg_dist, segments, spl)
    classes, segments = merge_seg(classes, segments)
#     print("classes_1: ", classes)
#     print("seg_1: ", segments)

    vel, acc, classes = clasify_segments(avg_dist, segments, spl)
    classes, segments = merge_seg(classes, segments)
#     print("classes: ", classes)
#     print("seg_2: ", segments)
    if plot:
        for i in range(len(segments)):
            ax.text((segments[i][0]/30 + segments[i][2]/30)/2, 20,
                    classes[i][0][0] + ", {}".format(i+1), rotation=90, alpha=1)
            ax.axvline(x=segments[i][0]/30, ls='--', alpha=.4, c='k')
        ax.axvline(x=segments[-1][2]/30, ls='--', alpha=.8, c='k')

    p = pd.Series([None]*len(data))
    for name, segment in zip(classes, segments):
#         print("name", name)
#         print("seg", segment)
        if name == 'Approaching':
            p.iloc[segment[0]:segment[2]] = 'Approaching'
        elif name == 'Following':
            p.iloc[segment[0]:segment[2]] = 'Following'
        elif name == 'flying pass':
            p.iloc[segment[0]:segment[2]] = 'flying pass'
        else:
            p.iloc[segment[0]:segment[2]] = 'Backing off'
    return p, vel, acc,classes, segments, spl(np.arange(len(data))/30)