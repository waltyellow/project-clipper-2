import { ProjectCliPage } from './app.po';

describe('project-cli App', function() {
  let page: ProjectCliPage;

  beforeEach(() => {
    page = new ProjectCliPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
