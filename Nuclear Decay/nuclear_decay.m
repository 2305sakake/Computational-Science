n = 250; % matrix of atoms will be nxn
years = 50;

NX_curr = ones(n); NY_curr = zeros(n); NZ_curr = zeros(n); % Logical arrays

function[NX,NY,NZ] = currentpop(PX,PY,NX,NY,NZ,n)
    X_decays = rand(n).*NX > (1-PX); % rand(n).*NX eliminates elements of NX that = 0
    NX = NX - X_decays; % Remove X elements that decayed from NX
    NY = NY + X_decays; % Add new Y elemnts to NY
    Y_decays = rand(n).*NY > (1-PY);
    NY = NY - Y_decays;
    NZ = NZ + Y_decays;
end

% Take input from user for half-lives
hlX = input("Half-life of X: ");
hlY = input("Half-life of Y: ");

% Convert half-lives to probabilities
PX = 1 - exp(-log(2)/hlX); PY = 1 - exp(-log(2)/hlY); 

% stores the years + 1 matrices for the animation
animation = zeros(n,n,years + 1); 

for t = 0:years
    pop_matrix = NX_curr+100*NY_curr+1000*NZ_curr; % Scales each matrix by a large amount to make them distinguishable
    animation(:,:,t+1) = pop_matrix; % store in animation array
    [NX_curr,NY_curr,NZ_curr] = currentpop(PX,PY,NX_curr,NY_curr,NZ_curr,n); % calculate new population
end

outputVideo = VideoWriter('decay.mp4', 'MPEG-4'); 
outputVideo.FrameRate=1;

open(outputVideo); % Open the video so we can write in it

figure;

for t = 0:years
    M = animation(:,:,t+1);
    image(M)
    axis equal tight; % Removes the automatic horizontal stretch from figure
    
    frame = getframe(gcf); % get the current frame displayed on the figure
    writeVideo(outputVideo, frame); % store the frame into outputVideo
    pause(0.2)
end

close(outputVideo); 