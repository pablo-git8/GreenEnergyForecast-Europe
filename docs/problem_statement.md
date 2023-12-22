### Project Summary: Schneider Electric Hackathon Challenge

#### Context
In the era of digital transformation, Schneider Electric introduces a challenge to contribute to sustainable computing. The aim is to predict which European country will have the highest surplus of green energy in the next hour. This initiative seeks to leverage this information for optimizing computing tasks, utilizing green energy efficiently, and thereby reducing carbon emissions.

#### Objective
The challenge involves creating a predictive model to identify the European country (among nine specified nations) with the highest green energy surplus in the forthcoming hour. The model should account for renewable energy generation (wind, solar, geothermic, etc.) and energy consumption. The key is to calculate the surplus as the difference between generated green energy and energy consumption, aligning with Schneider Electric's commitment to sustainability.

#### Dataset
Participants will work with hourly time-series data from the ENTSO-E Transparency portal. The data includes electricity consumption, wind, solar, and other green energy generation metrics for Spain, UK, Germany, Denmark, Sweden, Hungary, Italy, Poland, and the Netherlands. All data should be standardized to 1-hour intervals. Participants need to use the API to retrieve data from 01-01-2022 to 01-01-2023, preparing 'train.csv' and 'test.csv' datasets with an 80/20 training/testing split.