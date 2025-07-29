% Mon Jul 28 22:01:59 CDT 2025
% 
% call this function with the path to the matlab file to be loaded, e.g.:
% 
% octave:84> ostracodstats("1-3-25 Ostracod Runs Image 1/trackStore_001.mat")
%
% this function will export something with a format similar to the
% "ObjectXY.txt" files, but with the data from the matlab file.
function ostracodstats(f)
    data = load(f);
    disp(["loaded ", f])

    % create the output text file
    output_name = [f, '.txt'];
    output = fopen(output_name, 'w');

    for i = 1:size(data.tracksHist)(2)
        % extract the data, casting to integers just in case
        n = size(data.tracksHist(i).corrX)(1);
        x = int32(data.tracksHist(i).corrX(:,1));
        y = int32(data.tracksHist(i).corrX(:,4));
        frames = int32(data.tracksHist(i).corrFrame);

        % guess the path to the images folder based on the path to the .mat
        % file we just loaded. This is not necessary but just to keep with
        % convention.
        path_to_images = regexprep(f, "[^/]+[.]mat", "Images_001");

        % write one line per observation
        for j = 1:n
            % using printf with string and numeric data requires using cell
            % arrays (rather than regular arrays). Note that the image
            % filenames that this prints will likely not exist (in many cases)
            % since we're not actually exporting any images.
            output_data = {i, j, path_to_images, i, j, x(j), y(j), frames(j)};
            fprintf(output, "%4d, %4d, '%s/Object_%03d/Image_%03d.png', cX=%4d, cY=%4d, Frame=%6d\n", output_data{1,:});
        end

        % visualize the data
        %plot(x, y, 'x-');
        %pause;
    end

    fclose(output);

    disp(["wrote output to '", output_name, "'"]);
end
